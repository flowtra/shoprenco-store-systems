# TG Bot for order collection
## PROBLEM
When students/customers came to our shop in school to collect their orders, our senior EXCO relied on manually searching for their order number in Google Sheets to obtain their order information. This was then verbally shouted to ‘pickers’ who would collect the order and pass it to the customer. The process was slow and chaotic.
## SOLUTION
I developed a full-stack system beginning with a lightweight iOS QR Code Scanning app built on Swift, that would retrieve an order number from the QR Code. The app would then send a POST Request to a custom API which would then retrieve order details, and send it to an available picker via a telegram bot. Database used was MongoDB.
## IMPACT
This solution improved order collection efficiency by 400% from 30 orders/hour to 120 orders / hour – also reducing customer waiting times.
