<h1>Department News Board</h1>

Sebuah service yang dapat digunakan untuk membuat dan melihat berita.

How to run :
1. nameko run user
2. nameko run gateway
3. check in postman

Fungsi - fungsi yang ada :
1. /login - Untuk melakukan login agar dapat membuat berita
2. /register - Untuk dapat memiliki login dan melakukan fitur yang mebutuhkan login
3. /logout - Untuk menghapus session setelah melakukan login
4. /post_news - Untuk melakukan pembuatan/publish berita *membutuhkan login.
5. /update_news/<int:x> - Untuk melakukan pengeditan berita *membutuhkan login.
6. /delete_news/<int:x> - Untuk melalukan penghapusan berita yang ada *membutuhkan login.
7. /get_all_news - Untuk melakukan pengambilan semua data berita yang ada.
8. /get_news/<int:x> - Untuk melalukan pengambilan data news sesuai ID.

Untuk news yang diambil dalam jangka waktu tidak lebih dari 30 hari..
