# Task 2.1: Complete Use Case Diagram

```mermaid


flowchart LR
    %% Actors
    M((Member))
    NM((Non-Member))
    OPC((Order Processing\nClerk))
    CDC((Collection Dept\nClerk))

    subgraph ABCD Records System
        PO([Place Order])
        VM([Verify Membership])
        ProcessO([Process Order])
        MP([Make Payment])
        
        VIA([Verify Item Availability])
        AD([Apply Discount])
        PI([Print Invoice])
        PSL([Print Shipping List])
        OUI([Order Unavailable Items])
        SMA([Send Membership Application])
    end

    %% Actor to Use Case links
    M --- PO
    M --- MP
    NM --- PO
    OPC --- ProcessO
    CDC --- MP

    %% Includes (Mandatory)
    ProcessO -. "<<include>>" .-> VM
    ProcessO -. "<<include>>" .-> VIA
    ProcessO -. "<<include>>" .-> PI
    ProcessO -. "<<include>>" .-> PSL

    %% Extends (Conditional)
    SMA -. "<<extend>>\n(If non-member)" .-> VM
    AD -. "<<extend>>\n(If Royal)" .-> ProcessO
    OUI -. "<<extend>>\n(If Royal & Unavailable)" .-> VIA
```

# Task 2.2: Complete Class Diagram

```mermaid
classDiagram
    class Member {
        <<Abstract>>
        +String memberId
        +String name
        +String address
    }
    class RoyalMember {
        +Float discountRate
        +orderUnavailableItems()
    }
    class RegularMember {
    }
    Member <|-- RoyalMember
    Member <|-- RegularMember

    class Item {
        <<Abstract>>
        +String itemId
        +String title
        +Float price
        +bool isAvailable
    }
    class CD
    class Tape
    Item <|-- CD
    Item <|-- Tape

    class Payment {
        <<Abstract>>
        +String paymentId
        +Float amount
        +Date date
        +process() bool
    }
    class Cash
    class Check {
        +String checkNumber
    }
    class BankDraft {
        +String draftNumber
    }
    Payment <|-- Cash
    Payment <|-- Check
    Payment <|-- BankDraft

    class Order {
        +String orderId
        +Date date
    }
    class OrderLine {
        +Integer quantity
        +Float unitPrice
    }
    class Invoice {
        +String invoiceNumber
        +generate()
    }
    class ShippingList {
        +String listNumber
        +generate()
    }
    class MembershipApplication {
        +String tempId
        +sendTo(address: String)
    }

    Member "1" --> "0..*" Order : Places
    Order "1" *-- "1..*" OrderLine : Contains
    OrderLine "*" --> "1" Item : Refers to
    Order "1" --> "1" Invoice : Generates
    Order "1" --> "1" ShippingList : Generates
    Order "1" --> "1" Payment : Paid via
    MembershipApplication "*" <-- "1" OrderProcessingClerk : Sends to Non-Members


```



