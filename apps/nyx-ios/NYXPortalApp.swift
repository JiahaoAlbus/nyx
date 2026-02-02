import SwiftUI

@main
struct NYXPortalApp: App {
    @StateObject private var settings = BackendSettings()
    
    var body: some Scene {
        WindowGroup {
            AppShellView(settings: settings)
        }
    }
}
