from typing import List


class MpmsValue:
    value: str

    def __init__(self, value: str) -> None:
        self.value = value


class MpmsAttribute:
    id: int
    name: str
    values: List[MpmsValue]

    def __init__(self, id: int, name: str, values: List[MpmsValue]) -> None:
        self.id = id
        self.name = name
        self.values = values


class MpmsCategory:
    id: int
    name: str
    parentCategoryId: int
    parentCategory: str

    def __init__(self, id: int, name: str, parentCategoryId: int, parentCategory: str) -> None:
        self.id = id
        self.name = name
        self.parentCategoryId = parentCategoryId
        self.parentCategory = parentCategory


class MpmsSellerIntegratorData:
    id: int
    parentId: int
    productBrandName: str
    name: str
    description: str
    cest: str
    active: bool
    codeEAN: str
    codeNCM: int
    mainImageURL: str
    urlImages: List[str]
    productCode: str
    storeId: int
    attributes: List[MpmsAttribute]
    categories: List[MpmsCategory]

    def __init__(self, id: int,
                        parentId: int,
                        productBrandName: str,
                        name: str,
                        description: str,
                        cest: str,
                        active: bool,
                        codeEAN: str,
                        codeNCM: int,
                        mainImageURL: str,
                        urlImages: List[str],
                        productCode: str,
                        storeId: int,
                        attributes: List[MpmsAttribute],
                        categories: List[MpmsCategory]) -> None:
        self.id = id
        self.parentId = parentId
        self.productBrandName = productBrandName
        self.name = name
        self.description = description
        self.cest = cest
        self.active = active
        self.codeEAN = codeEAN
        self.codeNCM = codeNCM
        self.mainImageURL = mainImageURL
        self.urlImages = urlImages
        self.productCode = productCode
        self.storeId = storeId
        self.attributes = attributes
        self.categories = categories


class MpmsShippingDimensions:
    length: str
    width: str
    height: str
    weight: str

    def __init__(self, length: str, width: str, height: str, weight: str) -> None:
        self.length = length
        self.width = width
        self.height = height
        self.weight = weight


class MpmsProduct:
    itemid: str
    name: str
    gtins: List[int]
    shippingdimensions: MpmsShippingDimensions
    sellerintegratordataformat: str
    sellerintegratordata: MpmsSellerIntegratorData

    def __init__(self, itemid: str,
                        name: str,
                        gtins: List[int],
                        shippingdimensions: MpmsShippingDimensions,
                        sellerintegratordataformat: str,
                        sellerintegratordata: MpmsSellerIntegratorData) -> None:
        self.itemid = itemid
        self.name = name
        self.gtins = gtins
        self.shippingdimensions = shippingdimensions
        self.sellerintegratordataformat = sellerintegratordataformat
        self.sellerintegratordata = sellerintegratordata

class MpmsInventory:
    itemid: str
    stockid: str
    physicalquantity: int

    def __init__(self, itemid: str, stockid: str, physicalquantity: int) -> None:
        self.itemid = itemid
        self.stockid = stockid
        self.physicalquantity = physicalquantity

class MpmsPrice:
    itemid: str
    pricemsrp: str
    price: str

    def __init__(self, itemid: str, pricemsrp: str, price: str) -> None:
        self.itemid = itemid
        self.pricemsrp = pricemsrp
        self.price = price
