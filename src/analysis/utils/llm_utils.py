"""
LLM API请求处理工具模块
提供LLM调用和token统计功能
"""

import asyncio
from typing import Optional, Any
from astrbot.api import logger
import aiohttp


def get_provider_with_fallback(
    context, config_manager, provider_id_key: str, umo: str = None
) -> Optional[Any]:
    """
    根据配置键获取 Provider，支持多级回退

    回退顺序：
    1. 尝试从配置获取指定的 provider_id（如 topic_provider_id）
    2. 回退到主 LLM provider_id（llm_provider_id）
    3. 回退到当前会话的 Provider（通过 umo）
    4. 回退到第一个可用的 Provider

    Args:
        context: AstrBot上下文对象
        config_manager: 配置管理器
        provider_id_key: 配置中的 provider_id 键名（如 'topic_provider_id'）
        umo: unified_msg_origin，用于获取会话默认 Provider

    Returns:
        Provider 实例或 None
    """
    try:
        # 1. 尝试从配置获取特定任务的 provider_id
        specific_provider_id = None
        if provider_id_key:
            getter_method = f"get_{provider_id_key}"
            if hasattr(config_manager, getter_method):
                specific_provider_id = getattr(config_manager, getter_method)()
                if (
                    isinstance(specific_provider_id, str)
                    and specific_provider_id.strip()
                ):
                    specific_provider_id = specific_provider_id.strip()
                    logger.info(
                        f"尝试使用配置的 {provider_id_key}: {specific_provider_id}"
                    )
                    try:
                        provider = context.get_provider_by_id(
                            provider_id=specific_provider_id
                        )
                        if provider:
                            logger.info(
                                f"✓ 使用配置的特定 Provider: {specific_provider_id}"
                            )
                            return provider
                    except Exception as e:
                        logger.warning(
                            f"无法找到配置的 Provider ID '{specific_provider_id}': {e}"
                        )

        # 2. 回退到主 LLM provider_id
        main_provider_id = config_manager.get_llm_provider_id()
        if isinstance(main_provider_id, str) and main_provider_id.strip():
            main_provider_id = main_provider_id.strip()
            logger.info(f"尝试使用主 LLM Provider: {main_provider_id}")
            try:
                provider = context.get_provider_by_id(provider_id=main_provider_id)
                if provider:
                    logger.info(f"✓ 使用主 LLM Provider: {main_provider_id}")
                    return provider
            except Exception as e:
                logger.warning(f"无法找到主 LLM Provider ID '{main_provider_id}': {e}")

        # 3. 回退到当前会话的 Provider
        try:
            provider = context.get_using_provider(umo=umo)
            if provider:
                try:
                    meta = provider.meta()
                    provider_id = meta.id
                    logger.info(f"✓ 使用当前会话的 Provider: {provider_id}")
                except Exception:
                    logger.info("✓ 使用当前会话的默认 Provider")
                return provider
        except Exception as e:
            logger.warning(f"无法获取会话 Provider: {e}")

        # 4. 最后回退：使用第一个可用的 Provider
        try:
            all_providers = context.get_all_providers()
            if all_providers and len(all_providers) > 0:
                provider = all_providers[0]
                logger.info(f"✓ 使用第一个可用 Provider: {type(provider).__name__}")
                return provider
        except Exception as e:
            logger.warning(f"无法获取任何 Provider: {e}")

    except Exception as e:
        logger.error(f"Provider 选择过程出错: {e}")

    return None


async def call_provider_with_retry(
    context,
    config_manager,
    prompt: str,
    max_tokens: int,
    temperature: float,
    umo: str = None,
    provider_id_key: str = None,
) -> Optional[Any]:
    """
    调用LLM提供者，带超时、重试与退避。支持自定义服务商和配置化 Provider 选择。

    Args:
        context: AstrBot上下文对象
        config_manager: 配置管理器
        prompt: 输入的提示语
        max_tokens: 最大生成token数
        temperature: 采样温度
        umo: 指定使用的模型唯一标识符
        provider_id_key: 配置中的 provider_id 键名（如 'topic_provider_id'），用于选择特定的 Provider

    Returns:
        LLM生成的结果，失败时返回None
    """
    timeout = config_manager.get_llm_timeout()
    retries = config_manager.get_llm_retries()
    backoff = config_manager.get_llm_backoff()

    last_exc = None
    for attempt in range(1, retries + 1):
        try:
            # 使用新的 provider 选择逻辑，支持配置化选择和多级回退
            provider = get_provider_with_fallback(
                context, config_manager, provider_id_key, umo
            )

            provider_id = "unknown"
            if provider:
                try:
                    meta = provider.meta()
                    provider_id = meta.id
                except Exception as e:
                    logger.debug(f"获取提供商ID失败: {e}")

            if not provider:
                logger.error("provider 为空，无法调用 text_chat，直接返回 None")
                return None

            logger.info(
                f"使用LLM provider (ID: {provider_id}), max_tokens={max_tokens}, temperature={temperature}"
            )

            logger.debug(f"LLM provider prompt 长度: {len(prompt) if prompt else 0}")
            logger.debug(
                f"LLM provider prompt 前100字符: {prompt[:100] if prompt else 'None'}..."
            )

            # 检查 prompt 是否为空
            if not prompt or not prompt.strip():
                logger.error(
                    "LLM provider: prompt 为空或只包含空白字符，无法调用 text_chat"
                )
                return None

            coro = provider.text_chat(
                prompt=prompt, max_tokens=max_tokens, temperature=temperature
            )
            return await asyncio.wait_for(coro, timeout=timeout)
        except asyncio.TimeoutError as e:
            last_exc = e
            logger.warning(f"LLM请求超时: 第{attempt}次, timeout={timeout}s")
        except Exception as e:
            last_exc = e
            logger.warning(f"LLM请求失败: 第{attempt}次, 错误: {last_exc}")
        # 若非最后一次，等待退避后重试
        if attempt < retries:
            await asyncio.sleep(backoff * attempt)

    # 最终仍失败，记录错误并返回 None 由调用方处理降级，避免抛出异常
    logger.error(f"LLM请求全部重试失败: {last_exc}")
    return None


def extract_token_usage(response) -> Optional[dict]:
    """
    从LLM响应中提取token使用统计

    Args:
        response: LLM响应对象

    Returns:
        Token使用统计字典，包含prompt_tokens, completion_tokens, total_tokens
    """
    try:
        token_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

        # 安全地提取 usage，避免 response.raw_completion.usage 为 None 导致的 AttributeError
        usage = None
        if getattr(response, "raw_completion", None) is not None:
            usage = getattr(response.raw_completion, "usage", None)
            if usage:
                token_usage["prompt_tokens"] = getattr(usage, "prompt_tokens", 0) or 0
                token_usage["completion_tokens"] = (
                    getattr(usage, "completion_tokens", 0) or 0
                )
                token_usage["total_tokens"] = getattr(usage, "total_tokens", 0) or 0

        return token_usage

    except Exception as e:
        logger.error(f"提取token使用统计失败: {e}")
        return {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}


def extract_response_text(response) -> str:
    """
    从LLM响应中提取文本内容

    Args:
        response: LLM响应对象

    Returns:
        响应文本内容
    """
    try:
        if hasattr(response, "completion_text"):
            return response.completion_text
        else:
            return str(response)
    except Exception as e:
        logger.error(f"提取响应文本失败: {e}")
        return ""
