import SwiftUI

struct AppShellView: View {
    @ObservedObject var settings: BackendSettings
    @State private var selectedTab = 0
    
    var body: some View {
        TabView(selection: $selectedTab) {
            NYXHomeView(settings: settings)
                .tabItem {
                    Label("Home", systemImage: "house.fill")
                }
                .tag(0)
            
            NYXWalletView(settings: settings)
                .tabItem {
                    Label("Wallet", systemImage: "wallet.pass.fill")
                }
                .tag(1)
            
            NYXExchangeView()
                .tabItem {
                    Label("Exchange", systemImage: "arrow.left.arrow.right.circle.fill")
                }
                .tag(2)
            
            NYXChatView()
                .tabItem {
                    Label("Chat", systemImage: "bubble.left.and.bubble.right.fill")
                }
                .tag(3)
            
            NYXStoreView()
                .tabItem {
                    Label("Store", systemImage: "bag.fill")
                }
                .tag(4)
            
            NYXActivityView()
                .tabItem {
                    Label("Activity", systemImage: "clock.fill")
                }
                .tag(5)
            
            NYXEvidenceView()
                .tabItem {
                    Label("Evidence", systemImage: "shield.fill")
                }
                .tag(6)
            
            SettingsView(settings: settings)
                .tabItem {
                    Label("Settings", systemImage: "gearshape.fill")
                }
                .tag(7)
        }
        .accentColor(.blue)
    }
}

// MARK: - Native Views

struct NYXHomeView: View {
    @ObservedObject var settings: BackendSettings
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(alignment: .leading, spacing: 20) {
                    HStack {
                        VStack(alignment: .leading) {
                            Text("NYX Portal")
                                .font(.largeTitle)
                                .fontWeight(.bold)
                            Text("Testnet Beta")
                                .font(.caption)
                                .fontWeight(.bold)
                                .foregroundColor(.secondary)
                        }
                        Spacer()
                        Image(systemName: "diamond.fill")
                            .font(.system(size: 40))
                            .foregroundColor(.blue)
                    }
                    .padding(.horizontal)
                    
                    VStack(alignment: .leading, spacing: 10) {
                        Text("Status")
                            .font(.headline)
                        HStack {
                            Circle()
                                .fill(Color.green)
                                .frame(width: 10, height: 10)
                            Text("Backend Available")
                                .font(.subheadline)
                            Spacer()
                            Text(settings.baseURL)
                                .font(.caption)
                                .foregroundColor(.secondary)
                        }
                        .padding()
                        .background(Color(.secondarySystemBackground))
                        .cornerRadius(12)
                    }
                    .padding(.horizontal)
                    
                    VStack(alignment: .leading, spacing: 15) {
                        Text("Quick Actions")
                            .font(.headline)
                        
                        LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: 15) {
                            ActionCard(title: "Faucet", icon: "drop.fill", color: .blue)
                            ActionCard(title: "Scan", icon: "qrcode.viewfinder", color: .purple)
                            ActionCard(title: "Chat", icon: "bubble.left.and.bubble.right.fill", color: .green)
                            ActionCard(title: "Settings", icon: "gearshape.fill", color: .gray)
                        }
                    }
                    .padding(.horizontal)
                }
                .padding(.vertical)
            }
            .navigationBarHidden(true)
        }
    }
}

struct NYXWalletView: View {
    @ObservedObject var settings: BackendSettings
    @State private var balance: Int = 0
    @State private var address: String = "0x..."
    @State private var isLoading = false
    
    var body: some View {
        NavigationView {
            VStack(spacing: 25) {
                VStack(spacing: 10) {
                    Text("Total Balance")
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                    Text("\(balance) NYXT")
                        .font(.system(size: 40, weight: .bold, design: .rounded))
                }
                .padding(.top, 40)
                
                VStack(alignment: .leading, spacing: 15) {
                    Text("Your Address")
                        .font(.headline)
                    HStack {
                        Text(address)
                            .font(.system(.subheadline, design: .monospaced))
                            .lineLimit(1)
                        Spacer()
                        Button(action: {
                            UIPasteboard.general.string = address
                        }) {
                            Image(systemName: "doc.on.doc")
                                .foregroundColor(.blue)
                        }
                    }
                    .padding()
                    .background(Color(.secondarySystemBackground))
                    .cornerRadius(12)
                }
                .padding(.horizontal)
                
                HStack(spacing: 20) {
                    Button(action: requestFaucet) {
                        VStack {
                            Image(systemName: "arrow.down.circle.fill")
                                .font(.title)
                            Text("Faucet")
                                .font(.caption)
                                .fontWeight(.bold)
                        }
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Color.blue)
                        .foregroundColor(.white)
                        .cornerRadius(15)
                    }
                    
                    Button(action: {}) {
                        VStack {
                            Image(systemName: "arrow.up.circle.fill")
                                .font(.title)
                            Text("Send")
                                .font(.caption)
                                .fontWeight(.bold)
                        }
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Color.blue)
                        .foregroundColor(.white)
                        .cornerRadius(15)
                    }
                }
                .padding(.horizontal)
                
                VStack(alignment: .leading, spacing: 15) {
                    Text("Recent Activity")
                        .font(.headline)
                    
                    List {
                        Text("No recent transactions")
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                    .listStyle(PlainListStyle())
                }
                .padding(.horizontal)
                
                Spacer()
            }
            .navigationTitle("Wallet")
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(action: refresh) {
                        Image(systemName: "arrow.clockwise")
                    }
                }
            }
        }
        .onAppear(perform: refresh)
    }
    
    func refresh() {
        if address == "0x..." {
            address = "acct-" + UUID().uuidString.prefix(8).lowercased()
        }
        
        isLoading = true
        let client = GatewayClient(baseURL: URL(string: settings.baseURL)!)
        Task {
            do {
                let bal = try await client.fetchWalletBalance(address: address)
                DispatchQueue.main.async {
                    self.balance = bal
                    self.isLoading = false
                }
            } catch {
                print("Error fetching balance: \(error)")
                DispatchQueue.main.async {
                    self.isLoading = false
                }
            }
        }
    }
    
    func requestFaucet() {
        isLoading = true
        let client = GatewayClient(baseURL: URL(string: settings.baseURL)!)
        Task {
            do {
                _ = try await client.walletFaucet(seed: 123, runId: "faucet-\(Date.now.timeIntervalSince1970)", address: address, amount: 100)
                refresh()
            } catch {
                print("Faucet failed: \(error)")
                DispatchQueue.main.async {
                    self.isLoading = false
                }
            }
        }
    }
}

struct ActionCard: View {
    let title: String
    let icon: String
    let color: Color
    
    var body: some View {
        VStack {
            Image(systemName: icon)
                .font(.title)
                .foregroundColor(.white)
                .frame(width: 60, height: 60)
                .background(color)
                .cornerRadius(15)
            Text(title)
                .font(.caption)
                .fontWeight(.medium)
        }
        .frame(maxWidth: .infinity)
        .padding()
        .background(Color(.secondarySystemBackground))
        .cornerRadius(15)
    }
}

struct NYXExchangeView: View { var body: some View { Text("Exchange module active") } }
struct NYXChatView: View { var body: some View { Text("Chat module active") } }
struct NYXStoreView: View { var body: some View { Text("Store module active") } }
struct NYXActivityView: View { var body: some View { Text("Activity feed active") } }
struct NYXEvidenceView: View { var body: some View { Text("Evidence verified") } }
