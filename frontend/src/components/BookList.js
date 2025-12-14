import React from "react";

function BookList({ books }) {
  return (
    <div>
      <h2>Available Books</h2>
      <ul>
        {books.length > 0 ? (
          books.map((book) => (
            <li key={book.id}>
              {book.title} by {book.author}
            </li>
          ))
        ) : (
          <p>No books found.</p>
        )}
      </ul>
    </div>
  );
}

export default BookList;
