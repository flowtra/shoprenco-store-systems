//
//  SecondView.swift
//  storeapp
//
//  Created by Putra Zayan on 14/11/22.
//

import SwiftUI

struct Response: Codable {
    let _id: String
    let collected: String
    let orderName: String
    let payment_status: String
    var items: [Result]
}

struct Result: Hashable, Codable {
    let itemName: String
    let itemQuantity: Int
    
}

struct SecondView: View {
    @State private var _id = ""
    @State private var collected = ""
    @State private var results = [Result]()
    @State private var orderName = ""
    @State private var orderStatus = ""

    @Binding var scannedCode: String
    
    var body: some View {
        NavigationView {
            if orderStatus == "UNAVAILABLE" {
                Text("NOT READY")
                    .foregroundColor(Color.red)
                    .bold()
                    .multilineTextAlignment(.leading)
                    .listRowSeparator(.hidden)
            } else {
                List {
                    if orderStatus == "APPROVED" {
                        Text("APPROVED")
                            .foregroundColor(Color.green)
                            .bold()
                            .multilineTextAlignment(.leading)
                            .listRowSeparator(.hidden)
                    } else if orderStatus == "PENDING" {
                        Text("PENDING")
                            .foregroundColor(Color.yellow)
                            .bold()
                            .multilineTextAlignment(.leading)
                            .listRowSeparator(.hidden)
                    } else if orderStatus == "CANCELLED" {
                        Text("CANCELLED")
                            .foregroundColor(Color.red)
                            .bold()
                            .multilineTextAlignment(.leading)
                            .listRowSeparator(.hidden)
                    }
                    
                    ForEach(results, id: \.itemName) { result in
                        itemView(itemName: result.itemName, itemQuantity: result.itemQuantity)
                            .listRowSeparator(.hidden)
                    }
                }
                .listStyle(.plain)
                .navigationTitle(orderName.capitalized)
                .safeAreaInset(edge: .bottom) {
                    Button{
                        
                    } label: {
                        Text("Complete Order")
                            .foregroundColor(Color.white)
                            .font(.title)
                            .bold()
                    }
                    .frame(width: 400)
                    .padding(.vertical)
                    .background(Color.blue)
                }
            }
        }
        .task {
            await loadData()
            if orderStatus != "UNAVAILABLE" {
                await sendDataToDB()
            }
        }
    }
    
    func loadData() async {
        print("loading")
        guard let url = URL(string: "https://api.shopren.co/getSweaterCollectible?orderNo=\(scannedCode)") else
            {
            print("INVALID URL")
            return
        }
        
        do {
            let (data, _) = try await URLSession.shared.data(from: url)
            if let decodedResponse = try? JSONDecoder().decode(Response.self, from: data) {
                print(decodedResponse)
                _id = decodedResponse._id
                collected = decodedResponse.collected
                results = decodedResponse.items
                orderName = decodedResponse.orderName
                orderStatus = decodedResponse.payment_status
            }
        } catch {
            print("Invalid Data")
        }
    }
    
    func sendDataToDB() async {
        print("Sending data to db")
        guard let url = URL(string: "https://api.shopren.co/db/addSweaterOrder?orderNo=\(scannedCode)") else
            {
            print("INVALID URL")
            return
        }
        
        do {
            let (data, _) = try await URLSession.shared.data(from: url)
            if let decodedResponse = try? JSONDecoder().decode(Response.self, from: data) {
                print(decodedResponse)
            }
        } catch {
            print("Invalid Data")
        }
    }
}

struct SecondView_Previews: PreviewProvider {
    static var previews: some View {
        SecondView(scannedCode: .constant("No Code"))
    }
}
