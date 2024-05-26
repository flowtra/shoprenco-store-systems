//
//  ContentView.swift
//  storeapp
//
//  Created by Putra Zayan on 13/11/22.
//

import SwiftUI
import CodeScanner

struct ContentView: View {
    @State var isPresentingScanner = false
    @State var scannedCode: String = "71576255676249B4"
    @State private var showingSecondVC = false
    
    var scannerSheet : some View {
        CodeScannerView(
            codeTypes: [.qr],
            completion: { result in
                if case let .success(code) = result {
                    self.scannedCode = code.string
                    self.isPresentingScanner = false
                    let secondsToDelay = 0.1
                    DispatchQueue.main.asyncAfter(deadline: .now() + secondsToDelay) {
                        self.showingSecondVC.toggle()
                    }
                }
                
            }
        )
    }
    
    var body: some View {
        VStack(spacing: 10) {
            Text(scannedCode)
            Button("Scan QR Code") {
                self.isPresentingScanner = true
            }
            
            .sheet(isPresented: $isPresentingScanner) {
                self.scannerSheet
            }
            
            Button(action: {
                self.showingSecondVC.toggle()
                print("showing")
            }){
                Text("Retrieve Order")
            }.sheet(isPresented: $showingSecondVC){
                SecondView(scannedCode: $scannedCode)
            }
        }
        .padding()
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
