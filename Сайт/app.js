const express = require('express');
const path = require('path');
const app = express();

app.use(express.static(__dirname + '/public'));

// Явно прописанные маршруты для страниц
app.get('/articles', (req, res) => {
  res.sendFile(path.join(__dirname, './public/articles.html'));
});
app.get('/article', (req, res) => {
  res.sendFile(path.join(__dirname, './public/full_article.html'));
});
app.get('/calculator', (req, res) => {
  res.sendFile(path.join(__dirname, './public/calculator.html'));
});

app.get('/check_doc', (req, res) => {
  res.sendFile(path.join(__dirname, './public/check_doc.html'));
});

app.get('/articles_search', (req, res) => {
  res.sendFile(path.join(__dirname, './public/articles_search.html'));
});

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, './public/index.html'));
});

app.get('/form', (req, res) => {
  res.sendFile(path.join(__dirname, './public/form.html'));
});


app.use((req, res) => {
    res.redirect('/');
});

// Запуск сервера
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
