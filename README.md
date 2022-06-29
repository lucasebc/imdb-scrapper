# imdb-scrapper

Scrapper to save a list of movies in a .txt file and their cover images

## Scrapper IMDB

O script scrapper.py monta a url para busca dos filmes de acordo com as constantes:

- 'NUM_MOVIES' - quantidade de filmes a buscar
- 'COUNT' - quantidade de filmes a buscar por página. quanto menor o valor, mais chamadas serão feitas. Valor máx 250.
- 'NUM_PAGES' - quantidade de páginas para requisitar. Gerada a partir das outras 2.

Faz a busca das páginas, abre o html e busca os dados dos filmes listados.
Após finalizar a busca, pede ao usuário se deseja fazer a ordenação por qualquer dos 6 campos buscados, ascendente ou descendente.
Depois de ordenar os filmes, salva os 20 primeiros no arquivo 'Filmes.txt' e faz o download das capas/pôsteres para a pasta '/fotos/[id].png'.
Após gerar os arquivos, pede para o usuário se quer receber um email com o resultado. Caso sim, pede o e-mail que deve receber.
Para enviar o email, chama as funções do arquivo 'mail.py'. Lá é necessário colocar os valores das constantes 'SENDER_MAIL' e 'SENDER_PASS'. a função 'sendMail' recebe o email montado e o provedor do de envio de email, que pode ser 'outlook' e 'gmail'
