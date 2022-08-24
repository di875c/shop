const exampleModal = document.getElementById('galleryModal')
exampleModal.addEventListener('show.bs.modal', event => {
  // Кнопка, которая активировала модальное окно
  const button = event.relatedTarget
  // Извлекает информацию из атрибутов data-bs-*
  const recipient = button.getAttribute('data-bs-link')
  // При необходимости вы можете инициировать запрос AJAX здесь,
  // а затем выполнить обновление в обратном вызове.
  //
  // Обновляет содержимое модального окна.
  const modalImg = exampleModal.querySelector('.modal-img-fluid')

  modalImg.src = recipient
})
