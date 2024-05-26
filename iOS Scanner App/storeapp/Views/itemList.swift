//
//  itemList.swift
//  storeapp
//
//  Created by Putra Zayan on 14/11/22.
//

import SwiftUI

struct itemList: View {
    var body: some View {
        HStack(spacing: 20) {
            Image("greenshirt")
                .resizable()
                .aspectRatio(contentMode: .fit)
                .frame(width: 70)
            
            Text("1")

            
            VStack(alignment: .leading, spacing: 10) {
                Text("Green Raglan T-Shirt")
                    .font(.headline)
                
                Text("Small")
            }
            
            Spacer()
        }
        .padding(.horizontal)
        .frame(maxWidth: .infinity, alignment: .leading)
    }
}

struct itemList_Previews: PreviewProvider {
    static var previews: some View {
        itemList()
    }
}
