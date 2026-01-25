import os
import unittest
from pathlib import Path


class IOSProjectScaffoldTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(__file__).resolve().parents[1]
        self.project = self.root / "NYXPortal.xcodeproj" / "project.pbxproj"

    def test_project_exists(self) -> None:
        self.assertTrue(self.project.exists())

    def test_project_references_sources(self) -> None:
        text = self.project.read_text(encoding="utf-8")
        expected = [
            "NYXPortalApp.swift",
            "ContentView.swift",
            "ModuleViews.swift",
            "EvidenceBundle.swift",
            "ExchangeModels.swift",
            "MarketplaceModels.swift",
            "ChatModels.swift",
            "EntertainmentModels.swift",
            "WalletModels.swift",
            "GatewayClient.swift",
            "Info.plist",
            "Assets.xcassets",
        ]
        for name in expected:
            with self.subTest(name=name):
                self.assertIn(name, text)


if __name__ == "__main__":
    unittest.main()
