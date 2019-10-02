# Projeto-UFU-SD
Projeto feito para planejamento e implementação de uma aplicação usando Sisteamas Distribuídos. Trabalho para a matéria GBC074 da Universidade Federal de Uberlândia.

**Integrantes:** [Vinícius Henrique Almeida Praxedes](https://github.com/vinivosh), [Vitor Ramos Cardoso](https://github.com/vrcardoso/Trab_Sistemas_Distribuidos)

**Ideia inicial:** Um clone simplificado do [pixelcanvas.io](https://pixelcanvas.io/)

A ideia inicial do projeto é criar um clone extremamente simplificado do aplicativo web [pixelcanvas.io](https://pixelcanvas.io/), cujo código pode ser encontrado no [respectivo github](https://github.com/pixelcanvasio/pixelcanvas). Basicamente uma malha de pixels que pode ser editada, pixel a pixel, por diversos "jogadores" ao mesmo tempo. As mudanças são exibidas para todos os jogadores, atualizadas a cada quadro renderizado da interface.

A plataforma rodará num servidor e permitirá que clientes se conectem a ele. No servidor ficará guardada a malha de pixels mestre, que será passada para cada cliente a cada atualização da interface (quadros por segundo). Quando um cliente modifica um pixel, tal mudança é enviada ao servidor, e seu efeito é refletido na malha de pixels, que será então passada a cada cliente que estiver conectado, quando suas interfaces forem atualizadas (na renderização do próximo quadro).

**Testes a serem implementados:**
* Teste de concorrência: mostrar que múltiplos clientes podem editar e vizualizar pixels da malha simultaneamente sem problemas de concorrência;
* Demo das funcionalidades: mostrar que todas funcionalidades desejadas na aplicação funcionam como esperado;
* Teste de persistência: mostrar que os dados salvos na malha de pixels são mantidos e exibidos posteriormente de forma correta

**Funcionalidades:**
* Funcionalidade em máquinas diferentes
* Exibição da malha de pixels para todos clientes
* Capacidade de se editar a mesma, por qualquer cliente conectado
