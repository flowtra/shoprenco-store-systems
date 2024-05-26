//
//  itemView.swift
//  storeapp
//
//  Created by Putra Zayan on 14/11/22.
//

import SwiftUI

struct itemView: View {
    
    let itemName: String
    let itemQuantity: Int
    
    var body: some View {
        ZStack {
//            Color("Background")
//                .edgesIgnoringSafeArea(.all)
            VStack {
                HStack {
                    VStack(alignment: .leading) {
                        if itemName.contains("Green Raglan") {
                            Image("greenshirt")
                                .resizable()
                                .frame(width: 50, height: 65)
                                .aspectRatio(contentMode: .fill)
                                .padding(.vertical)
                                .offset(y:3)
                        } else if itemName.contains("Singlet") {
                            Image("singlet")
                                .resizable()
                                .frame(width: 50, height: 65)
                                .aspectRatio(contentMode: .fill)
                                .padding(.vertical)
                                .offset(y:3)
                        } else if itemName.contains("Laptop") {
                            Image("greenshirt")
                                .resizable()
                                .frame(width: 50, height: 65)
                                .aspectRatio(contentMode: .fill)
                                .padding(.vertical)
                                .offset(y:3)
                        } else if itemName.contains("Black Dri-Fit") || itemName.contains("Black Cotton") {
                            Image("blackshirt")
                                .resizable()
                                .frame(width: 50, height: 65)
                                .aspectRatio(contentMode: .fill)
                                .padding(.vertical)
                                .offset(y:3)
                        } else if itemName.contains("Black Sweater") {
                            Image("sweater_black")
                                .resizable()
                                .frame(width: 74, height: 65)
                                .aspectRatio(contentMode: .fit)
                                .padding(.vertical)
                                .offset(y:3)
                        } else if itemName.contains("White Sweater") {
                            Image("sweater_white")
                                .resizable()
                                .frame(width: 73, height: 65)
                                .aspectRatio(contentMode: .fit)
                                .padding(.vertical)
                                .offset(y:3)
                        } else if itemName.contains("Cream Sweater") {
                            Image("sweater_cream")
                                .resizable()
                                .frame(width: 73, height: 65)
                                .aspectRatio(contentMode: .fit)
                                .padding(.vertical)
                                .offset(y:3)
                        }
                        
                    }
                    Spacer()
                        .frame(width: 20)
                    VStack(alignment: .leading) {
                        Text(itemName)
                            .font(.title2)
                            .bold()
                            .frame(alignment: .topLeading)
                        Spacer()
                            .frame(height:3)
//                        Text("Small")
//                            .font(.subheadline)
//                            .foregroundColor(Color.gray)
//                            .frame(alignment: .leading)
                        Spacer()
                            .frame(height:8)
                        Text("Quantity")
                            .font(.caption)
                            .foregroundColor(.gray)
                        Text("\(itemQuantity)")
                            .font(.headline)

                        
                    }


                }
                .frame(maxWidth: .infinity, alignment: .leading)
                .padding()
                .background(Color.gray.opacity(0.1), in: RoundedRectangle(cornerRadius: 10, style: .continuous))
                .padding(.horizontal, 4)
            }
        }
    }
    
}

struct itemView_Previews: PreviewProvider {
    static var previews: some View {
        itemView(itemName: "", itemQuantity: 0)
        itemView(itemName: "", itemQuantity: 0)
            .environment(\.colorScheme, .dark)
    }
}
