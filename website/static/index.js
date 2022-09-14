function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ id: noteId }),
  }).then((res) => {
    window.location.href = "/";
  });
}
