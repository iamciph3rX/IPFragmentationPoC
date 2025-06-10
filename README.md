# IPFragmentationPoC
ip fragmentation for pentest

//////////////

Fala, pessoal! 👋

Acabei de soltar uma POC que explora uma técnica que muitos firewalls modernos ainda não tratam direito: fragmentação de pacotes IP. Basicamente, o que fiz foi criar um script que fatiar uma requisição TCP legítima em vários pedaços e manda esses fragmentos de um jeito que o filtro pode não conseguir remontar direito — e aí, a mágica acontece: o payload potencialmente malicioso passa pela defesa sem ser barrado.

Por que isso importa?
Porque enquanto a galera foca em payloads sofisticados, muita gente esquece da “porta dos fundos” que são esses fragmentos IP mal tratados. É aquela falha que, na prática, pode ser a diferença entre um pentest amador e um pentest avançado.

Se você manja de segurança, já sabe: conhecer essas brechas faz toda a diferença na hora de montar uma boa estratégia de ataque ou defesa.

Essa PoC é pra quem quer ir além, testar o que poucos testam, e realmente entender onde estão as falhas invisíveis das redes.

Caso tenham dúvidas e vontade de conversar comigo, contatar meu discord;
**.cipherxx**
