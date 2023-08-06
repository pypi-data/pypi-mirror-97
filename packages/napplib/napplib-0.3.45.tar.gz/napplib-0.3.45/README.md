## **NappLIB**

NappLib
https://pypi.org/project/napplib/

## **Sobre**

Nós criamos essa biblioteca para auxiliar na integração dos nosso serviços e parceiros:

- Serviços Azure
- Napp HUB
- FTP e Base de dados remotas
- Conexoes com Webservices
- Plataformas de Marketplace

## **Funções**

### **Construir**

Abra o arquivo **setup.py** e altere a versão, após a mudança basta executar o arquivo abaixo:

```
./build.sh
```

### **Instalação**

```
pip install napplib
```

### **Azure Storage**

```python
from napplib.azure.blob_storage import BlobStorage
```

Função para retornar os dados do ultimo arquivo blob

```python
BlobStorage.get_latest_blob(
    account_name='AZURE_ACCOUNT_NAME',
    account_key='AZURE_ACCOUNT_KEY',
    path='AZURE_BLOB_ROOT_CONTAINER',
    project='PROJECT_NAME',
    store_name='STORE_NAME')
```

**Obs:** Vocë poderá adicionar o parametro **custom_encoding** caso seja diferente de **utf8**

Função para retornar os dados de um arquivo blob específico.

```python
BlobStorage.get_blob(
    account_name='AZURE_ACCOUNT_NAME',
    account_key='AZURE_ACCOUNT_KEY',
    path='AZURE_BLOB_ROOT_CONTAINER',
    blob_path='project/store/2020/10/23/sample.csv')
```

**Obs:** Vocë poderá adicionar o parametro **custom_encoding** caso seja diferente de **utf8**

Função que envia um arquivo local para o azure blob storage utilizando o modelo Napp, Ex: *project/store/year/month/day/file*. Temos algumas *flags* importantes, **first_charge** altera o nome do arquivo para uma nomenclatura de primeira carga (utilizado quando precisamos enviar muitos dados). **is_sale** altera o nome do arquivo para uma nomenclatura de vendas. **is_stock** altera o nome do arquivo para uma nomenclatura de estoque. Também adicionamos o "prefix" que podera compor o nome do arquivo da maneira que preferir, ex: "LOJA1-" ou "LOJA1_"

```python
BlobStorage.upload_blob(
    account_name='AZURE_ACCOUNT_NAME',
    account_key='AZURE_ACCOUNT_KEY',
    path='AZURE_BLOB_ROOT_CONTAINER',
    project='PROJECT_NAME',
    store_name='STORE_NAME',
    output_file='./files/sample.csv',
    prefix='',
    first_charge=False,
    is_sale=False,
    is_stock=False)
```

Lista todos arquivos blob de um determinado "projeto/loja"

```python
BlobStorage.list_all_blobs(
    account_name='AZURE_ACCOUNT_NAME',
    account_key='AZURE_ACCOUNT_KEY',
    path='AZURE_BLOB_ROOT_CONTAINER',
    project='PROJECT_NAME',
    store_name='STORE_NAME')
```

Para "parsear" os dados, poderá usar o seguinte modelo

```python
delimiter = '|'
lines = content.split('\n')
for line in lines:
    rows = line.split(delimiter)
    try:
        # parse here, rows[0], rows[1] ...
    except:
        # invlid line (always has one line empty)
        pass
```

**Obs**: *O split devera ocorrer por linha devido ao retorno do arquivo*

### **Napp HUB**

Importar todos modelos e controles

```python
from napplib.hub.models.product import Product
from napplib.hub.models.product import StoreProduct
from napplib.hub.models.order import Order
from napplib.hub.models.order import OrderShipping
from napplib.hub.models.order import OrderShippingAddress
from napplib.hub.models.order import OrderShippingItem
from napplib.hub.models.order import OrderCustomer
from napplib.hub.models.order import OrderCustomerAddress
from napplib.hub.models.order import OrderPayment
from napplib.hub.models.order import OrderAddress
from napplib.hub.models.order import OrderProduct
from napplib.hub.models.order import Invoice
from napplib.hub.models.order import InvoiceItem
from napplib.hub.controller import HubController
```

Variáveis necessárias para usar este controle

```python
hub_store_id = 0
hub_username = ''
hub_password = ''
hub_url = ''
```

Esta função cria todos objetos no Napp HUB  responsáveis para integrar um produto. Será necessário criar todos modelos abaixo

- product
- store product
- categories
- brands
- attributes

Essa função possui alguns gatilhos que podem ser utilizados

- **update_product**:  Esse gatilho atualiza o produto (product) quando verdadeiro, quando falso o controle ira somente criar o produto e não atualiza-lo caso exista.
- **update_store_product****: Esse gatilho atualiza o estoque da loja (storeProduct) quando verdadeiro, quando falso o controle ira somente criar o inventário e não atualiza-lo caso exista.

**Função**

```python
HubController.create_products(
    server_url=hub_url,
    token=hub_token,
    store_id=hub_store_id,
    products=hub_products,
    use_sku=True,
    update_product=True,
    update_store_product=True)
```

**Modelo StoreProduct**

```python

store_product = StoreProduct(
    storeId=HUB_STORE_ID,
    stockQuantity=0,
    salePrice=0,
    active=True,
    productCode='',
    productEan='',
    erpCode='',
    height=1,
    width=1,
    length=1,
    weight=1,
    measurementUnit='')
```

**Modelo Product**

```python
hub_product = Product(
    name='',
    description='',
    active=True,
    mainImageURL='',
    productCode='',
    productEan='',
    skuErp='',
    storeId=HUB_STORE_ID,
    attributes=[],
    categories=[],
    productBrandId=0,
    storeProduct=store_product)
```

**Modelo Payments**

```python
payments = []
order_payment = OrderPayment(
    amount='TOTAL', 
    date='DATA PAGAMENTO', 
    status='STATUS DO PAGAMENTO'
    planId='QUANTIDADE DE PARCELA'
    methodId='METODO DE PAGAMENTO CADASTRADO NO HUB'
order_payment = order_payment.__dict__
payments.append(order_payment)
```

**Modelo OrderProduct**

```python
# order item
order_items = []
order_item = OrderProduct(
    quantity='QUANTIDADE',
    salePrice='PRECO DE VENDA (FLOAT)',
    listPrice='PRECO DE TABELA',
    productDescription='DESCRICAO DO PRODUTO',
    productCode='SKU OU CODIGO DO PRODUTO',
    giftWrap='TRUE FALSE GIFT CARD'
)  
order_item = order_item.__dict__   
order_items.append(order_item)
```

**Modelo Invoices / InvoiceItem**

```python
# invoice item
invoice_items = []
invoice_item = InvoiceItem(
    productName='NOME DO PRODUTO', 
    productCode='SKU OU CODIGO DO PRODUTO', 
    quantity='QUANTIDADE', 
    value='PRECO DE VENDA', 
    totalValue='PRECO PAGO APLICADO DESCONTO'
)
invoice_item = invoice_item.__dict__
invoice_items.append(invoice_item)

invoices = []
order_invoice = Invoice(
    key='CHAVE DA NOTA',
    number='NUMERO DA NOTA'
    issueDate='DATA DA NOTA',
    orderForeignId='ID DA VENDA NO PDV',
    storeId='HUB_STORE_ID',
    itens=invoice_items,
    totalItens='QUANTIDADE TOTAL DE ITENS', 
    totalValue='TOTAL DA NOTA'
)
order_invoice = order_invoice.__dict__
invoices.append(order_invoice)
```

**Modelo OrderCustomerAddress / OrderCustomer**

```python
# create customer address
customer_addresses = []
customer_address = OrderCustomerAddress(
    address='ENDERECO', 
    addressNumber='NUMERO',
    city='CIDADE',
    country='PAIS (USAR SEMPRE O CODIGO, EX: BR)',
    zipCode='CODIGO POSTAL',
    reference='REFERENCIA',
    neighborhood='VIZINHANCA'
)
customer_address = customer_address.__dict__
customer_addresses.append(customer_address)

# create customer
customer = OrderCustomer(
    document='CPF/CNPJ',
    mainNumber='TELEFONE 1',
    secundaryNumber='TELEFONE 2',
    name='NOME',
    gender='M (MASCULINO), F (FEMININO)',
    birthDate='DATA DE ANIVERSARIO',
    email='EMAIL',
    type='PJ OU PF',
    addresses=customer_addresses)
customer = customer.__dict__
```

**Modelo OederAddress**

```python
# create order address
order_address = OrderAddress(
    billingName='NOME DO CLIENTE NA COBRANCA', 
    billingPhoneNumber='TELEFONE 1', 
    billingAddress='ENDERECO',
    billingAddressNumber='NUMERO',
    billingNeighborhood='VIZINHANCA',
    billingCity='CIDADE',
    billingState='ESTADO (EX: SP)',
    billingZipCode='CODIGO POSTAL',
    billingCountry='CODIGO DO PAIS (EX: BR)',
    billingReference='REFERENCIA',
    deliveryName='NOME DO CLIENTE PARA ENTREGA',
    deliveryAddress='ENDERECO ENTREGA',
    deliveryAddressNumber='NUMERO',
    deliveryPhoneNumber='TELEFONE 1',
    deliveryNeighborhood='VIZINHANCA',
    deliveryCity='CIDADE',
    deliveryState='ESTADO (EX: SP)',
    deliveryZipCode='CODIGO POSTAL',
    deliveryCountry='CODIGO DO PAIS (EX: BR)',
    deliveryReference='REFERENCIA'
)
order_address = order_address.__dict__
```

**Modelo Shipping, ShippingAddress e ShippingItem**

```python
# create shipping address
shipping_address = OrderShippingAddress(
    deliveryName='',
    deliveryAddress='',
    deliveryAddressNumber='',
    deliveryPhoneNumber='',
    deliveryNeighborhood='',
    deliveryCity='',
    deliveryState='',
    deliveryZipCode='',
    deliveryCountry='',
    deliveryReference=''
)
shipping_address = shipping_address.__dict__

# create shipping items
shipping_items = []
item = OrderShippingItem(
    quantity='',
    salePrice='',
    productDescription='',
    giftWrap='',
    productCode=''
)
item = item.__dict__
shipping_items.append(item)

# create shippings
shippings = []
shipping = OrderShipping(
    method='',
    estimateDeliveryDate='',
    carrierName='',
    shippingDate='',
    address='',
    trackingCode='',
    trackingURL='',
    itens=shipping_items
)
shipping = shipping.__dict__
shippings.append(shipping)    

```

**Modelo Order**

```python
order = Order(
    id='',
    storeId='', 
    orderStatus='', 
    marketplaceId='', 
    purchasedAt='',
    approvedAt='',
    updatedAt='',
    estimatedDeliveryDate='',
    totalAmount='',
    totalFreight='',
    totalDiscount='',
    totalTax='',
    totalItens='',
    deliveredDate='',
    contactName='',
    contactTelephoneNumber='',
    orderForeignId='',
    channelOrigin='',
    products=order_items,
    invoices=invoices,
    payments=payments,
    shippings=shippings,
    customer=customer,
    orderAddress=order_address
)
order = order.__dict__
```

### Criar os objetos Shipping, Invoice e Payments

```python
HubController.create_order_shipping(
    server_url=hub_url,
    token=token,
    shipping=shipping
) 

HubController.create_order_invoice(
    server_url=hub_url,
    token=token,
    invoice=invoice
)

  HubController.create_order_payment(
      server_url=hub_url,
      token=token,
      payment=payment
  )
```

### Criar e Atualizar Pedidos / Vendas

```python
# return ID to check success
update_id = HubController.update_order(
    server_url=hub_url,
    token=token,
    order=order
)

# return id to update orderId on objects like invoices, payments and shipments.
create_id = HubController.create_order(
    server_url=hub_url,
    token=token,
    order=order
)
```

### Verificar se o pedido existe no Napp HUB

```python
# search order date, format dd/MM/yyyy, Ex: 01/01/2021
search_date = ''

hub_order = HubController.get_order_by_foreign_id(
    server_url='HUB URL',
    token='HUB TOKEN',
    orderForeignId='ORDER ID',
    storeId='HUB STORE ID',
    purchasedAt=search_date
)

# create some variables
update = False
orderId = 0

# check if oder ID is != 0
if int(hub_order.get('id')) != 0:
    # enable update
    update = True
    
    # get orderId to use on update objects
    orderId = hub_order.get('id')
```

### **Vtex**

Importar todos modelos e controles

```python
from napplib.vtex.models.product import VtexProduct
from napplib.vtex.models.product import VtexSku
from napplib.vtex.models.product import VtexPrice
from napplib.vtex.models.product import VtexInventory
from napplib.vtex.models.product import VtexImage
from napplib.vtex.controller import VtexController
```

Variáveis necessárias para usar este controle

```python
vtex_store = ''
vtex_url = f'https://{vtex_store}.vtexcommercestable.com.br/api'
vtex_price_url = f'https://api.vtex.com/{vtex_store}/pricing'
vtex_app_key = ''
vtex_app_token = ''
```

Função do controle que cria todos objetos de produto na Vtex, será necessário criar os respectivos modelos

- product
- sku
- price
- inventory
- image

**Função**

```python

VtexController.create_products(
    base_url=vtex_url,
    base_url_price=vtex_price_url,
    app_key=vtex_app_key,
    app_token=vtex_app_token,
    products=vtex_product)
```

**Modelo Price**

```python
vtex_price = VtexPrice(
    listPrice=0,
    costPrice=0)
```

**Modelo Inventory**

```python
vtex_inventory = VtexInventory(quantity=0)
```

**Modelo Image**

```python
vtex_image = VtexImage(
    IsMain=True,
    Label='',
    Name='',
    Url='',
    Text='')
```

**Modelo SKU**

```python
vtex_sku = VtexSku(
    IsActive=True,
    Name='',
    RefId='',
    CreationDate='',
    MeasurementUnit='',
    price=vtex_price,
    inventory=vtex_inventory,
    images=vtex_image)
```

**Modelo Product**

```python
vtex_product = VtexProduct(
    Name='',
    CategoryId=0,
    BrandId=0,
    RefId='',
    IsVisible=True,
    Description='',
    DescriptionShort='',
    ReleaseDate='',
    Title='',
    IsActive=True,
    skus=vtex_sku)
```

### **Shopify**
-- 
### **MPMS**
--
### **OpaBox**
--
### **Yami**
--
### **FTP**

Importar todos os modelos e controles

```python
from napplib.ftp.controller import FTPController
```
Responsável por realizar a transferência de arquivos que chegam no ambiente FTP para o diretório local selecionado. Abaixo segue um exemplo de utilização:

```python
def download_ftp_files():
    if not os.path.exists(f'{current_path}/files'):
        os.mkdir(f'{current_path}/files')
        
    ftp_files = FTPController.download_ftp(
        host="www.ftpserver.com", # Endereco do ambiente
        login="user", # Usuario criado
        password="password", # Senha do usuario
        port="21", # Porta
        download_path=f'{current_path}', # Pasta de download
        extension=['csv'], # Extensao do arquivo a ser baixado
        move_downloaded_files=True # Parametro para mover arquivo apos baixado
    )

download_ftp_files()
```

### **Gmail**

Importar todos modelos e controles

```python
from napplib.google.GetAttachments import GetAttachments
```

Responsavel por realizar o download de arquivos enviados para o gmail. Abaixo um exemplo de utilizacao:

```python
from napplib.google.GetAttachments import GetAttachments

get_attachments = GetAttachments(
    query="subject: teste from: (test@gmail.com)",
    amount=1,
    pattern=None,
    download_folder='files'
)
get_attachments()

#create Path for download_path
path = Path('files')

# get files with extension (.xls)
for file in path.glob('*.xls'):
    print(f"Reading file {file}")
```

## **Desenvolvedor**

```
Napp Brain 🧠
leandro@nappsolutions.com
```