import yaml
from pathlib import Path
from typing import Dict, Any
from loguru import logger


class ConfigLoader:
    @staticmethod
    def list_available() -> list[str]:
        """Возвращает список доступных конфигураций"""
        config_dir = Path(__file__).parent.parent / "configs"
        logger.info(config_dir)
        logger.debug(f"config_dir: {config_dir}")
        return [f.stem for f in config_dir.glob("*.yaml")]

    @staticmethod
    def load(site_name: str) -> Dict[str, Any]:
        """Загружает конфигурацию для указанного сайта"""
        config_path = Path(__file__).parent.parent / "configs" / f"{site_name}.yaml"
        logger.info(f"config_path: {config_path}")

        if not config_path.exists():
            raise FileNotFoundError(f"Конфигурация для сайта '{site_name}' не найдена")


        with open(config_path, 'r', encoding='utf-8') as f:
            logger.info(f"Config for  {site_name} load successfully")
            return yaml.safe_load(f)

