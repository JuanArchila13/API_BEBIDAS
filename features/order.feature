Feature: Pedir bebidas desde el frontend React

  Como cliente
  Quiero pedir una bebida específica
  Para verificar si fue aceptada correctamente por el sistema

  Scenario: Pedido exitoso de bebida existente
    Given que la bebida "Capuccino" está registrada en el menú
    When realizo un pedido de "Capuccino" desde la API de pedidos
    Then el sistema debe aceptar el pedido con un código 200 o 201

  Scenario: Pedido fallido de bebida no existente
    Given que la bebida "Jugo de tomate de arbol" no está registrada en el menú
    When realizo un pedido de "Jugo de tomate de arbol" desde la API de pedidos
    Then el sistema debe rechazar el pedido con un código 404 o mensaje de error
