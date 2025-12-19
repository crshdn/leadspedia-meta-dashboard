"""
Configuration manager for dynamic campaign mappings.

This module handles the storage and retrieval of campaign-to-vertical
mappings in a local JSON file, separate from the .env configuration.
"""

from __future__ import annotations

import json
import os
import stat
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class CampaignVerticalMapping:
    """Maps a Meta campaign to a Leadspedia vertical."""
    
    meta_campaign_id: str
    meta_campaign_name: str
    vertical_id: str
    vertical_name: str
    min_sell_rate: float = 95.0
    min_roi: float = 20.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "meta_campaign_id": self.meta_campaign_id,
            "meta_campaign_name": self.meta_campaign_name,
            "vertical_id": self.vertical_id,
            "vertical_name": self.vertical_name,
            "min_sell_rate": self.min_sell_rate,
            "min_roi": self.min_roi,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CampaignVerticalMapping":
        return cls(
            meta_campaign_id=data["meta_campaign_id"],
            meta_campaign_name=data.get("meta_campaign_name", ""),
            vertical_id=data["vertical_id"],
            vertical_name=data.get("vertical_name", ""),
            min_sell_rate=float(data.get("min_sell_rate", 95.0)),
            min_roi=float(data.get("min_roi", 20.0)),
        )


@dataclass
class CampaignConfig:
    """Configuration for campaign mappings."""
    
    affiliate_id: str = ""
    mappings: List[CampaignVerticalMapping] = field(default_factory=list)
    default_vertical_id: Optional[str] = None
    default_min_sell_rate: float = 95.0
    default_min_roi: float = 20.0

    def get_mapping(self, meta_campaign_id: str) -> Optional[CampaignVerticalMapping]:
        """Get mapping for a specific Meta campaign."""
        for mapping in self.mappings:
            if mapping.meta_campaign_id == meta_campaign_id:
                return mapping
        return None

    def get_vertical_id(self, meta_campaign_id: str) -> Optional[str]:
        """Get vertical ID for a Meta campaign, falling back to default."""
        mapping = self.get_mapping(meta_campaign_id)
        if mapping:
            return mapping.vertical_id
        return self.default_vertical_id

    def to_dict(self) -> Dict[str, Any]:
        return {
            "affiliate_id": self.affiliate_id,
            "mappings": [m.to_dict() for m in self.mappings],
            "default_vertical_id": self.default_vertical_id,
            "default_min_sell_rate": self.default_min_sell_rate,
            "default_min_roi": self.default_min_roi,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CampaignConfig":
        return cls(
            affiliate_id=data.get("affiliate_id", ""),
            mappings=[CampaignVerticalMapping.from_dict(m) for m in data.get("mappings", [])],
            default_vertical_id=data.get("default_vertical_id"),
            default_min_sell_rate=float(data.get("default_min_sell_rate", 95.0)),
            default_min_roi=float(data.get("default_min_roi", 20.0)),
        )


class ConfigManager:
    """Manages campaign configuration stored in a local JSON file."""
    
    DEFAULT_CONFIG_PATH = Path(".config/campaign_mappings.json")
    
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or self.DEFAULT_CONFIG_PATH
        self._config: Optional[CampaignConfig] = None

    def _ensure_directory(self) -> None:
        """Ensure the config directory exists with proper permissions."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        # Set directory permissions to 700 (owner only)
        try:
            os.chmod(self.config_path.parent, stat.S_IRWXU)
        except OSError:
            pass  # May fail on some systems

    def _set_file_permissions(self) -> None:
        """Set file permissions to 600 (owner read/write only)."""
        try:
            os.chmod(self.config_path, stat.S_IRUSR | stat.S_IWUSR)
        except OSError:
            pass

    def load(self) -> CampaignConfig:
        """Load configuration from file."""
        if self._config is not None:
            return self._config
        
        if not self.config_path.exists():
            self._config = CampaignConfig()
            return self._config
        
        try:
            with open(self.config_path, "r") as f:
                data = json.load(f)
            self._config = CampaignConfig.from_dict(data)
        except (json.JSONDecodeError, KeyError, TypeError):
            self._config = CampaignConfig()
        
        return self._config

    def save(self, config: CampaignConfig) -> None:
        """Save configuration to file."""
        self._ensure_directory()
        
        with open(self.config_path, "w") as f:
            json.dump(config.to_dict(), f, indent=2)
        
        self._set_file_permissions()
        self._config = config

    def add_mapping(
        self,
        meta_campaign_id: str,
        meta_campaign_name: str,
        vertical_id: str,
        vertical_name: str,
        min_sell_rate: float = 95.0,
        min_roi: float = 20.0,
    ) -> None:
        """Add or update a campaign mapping."""
        config = self.load()
        
        # Remove existing mapping for this campaign if any
        config.mappings = [m for m in config.mappings if m.meta_campaign_id != meta_campaign_id]
        
        # Add new mapping
        config.mappings.append(CampaignVerticalMapping(
            meta_campaign_id=meta_campaign_id,
            meta_campaign_name=meta_campaign_name,
            vertical_id=vertical_id,
            vertical_name=vertical_name,
            min_sell_rate=min_sell_rate,
            min_roi=min_roi,
        ))
        
        self.save(config)

    def remove_mapping(self, meta_campaign_id: str) -> None:
        """Remove a campaign mapping."""
        config = self.load()
        config.mappings = [m for m in config.mappings if m.meta_campaign_id != meta_campaign_id]
        self.save(config)

    def set_affiliate_id(self, affiliate_id: str) -> None:
        """Set the affiliate ID."""
        config = self.load()
        config.affiliate_id = affiliate_id
        self.save(config)

    def set_default_vertical(self, vertical_id: Optional[str]) -> None:
        """Set the default vertical for unmapped campaigns."""
        config = self.load()
        config.default_vertical_id = vertical_id
        self.save(config)

    def set_default_thresholds(self, min_sell_rate: float, min_roi: float) -> None:
        """Set default alert thresholds."""
        config = self.load()
        config.default_min_sell_rate = min_sell_rate
        config.default_min_roi = min_roi
        self.save(config)

    def reload(self) -> CampaignConfig:
        """Force reload configuration from file."""
        self._config = None
        return self.load()

