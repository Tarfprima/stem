document.addEventListener('DOMContentLoaded', () => {
  // Находим модальное окно и его элементы
  const modal = document.getElementById('taskModal');
  const modalCloseBtn = document.getElementById('modalCloseBtn');
  const modalContent = document.getElementById('modalContent');
  const modalTitle = document.querySelector('.modal-task-title');
  const modalIcon = document.querySelector('.modal-task-icon');
  const modalCreated = document.getElementById('modalCreated');
  const modalReminder = document.getElementById('modalReminder');
  const modalReminderTime = document.getElementById('modalReminderTime');

  // Функция для открытия модального окна
  function openModal(taskData) {
    modalTitle.textContent = taskData.title;
    modalIcon.textContent = taskData.icon;
    modalContent.textContent = taskData.description;
    modalCreated.textContent = taskData.created;
    
    if (taskData.reminderTime) {
      modalReminderTime.textContent = taskData.reminderTime;
      modalReminder.style.display = 'block';
    } else {
      modalReminder.style.display = 'none';
    }
    
    modal.classList.add('show');
    document.body.style.overflow = 'hidden'; // Предотвращаем скролл фона
  }

  // Функция для закрытия модального окна
  function closeModal() {
    modal.classList.remove('show');
    document.body.style.overflow = ''; // Восстанавливаем скролл
  }

  // Обработчики для закрытия модального окна
  modalCloseBtn.addEventListener('click', closeModal);
  
  modal.addEventListener('click', (e) => {
    if (e.target === modal) { // Клик по overlay (вне модального окна)
      closeModal();
    }
  });
  
  // Закрытие по клавише Escape
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.classList.contains('show')) {
      closeModal();
    }
  });

  // Обрабатываем каждую карточку задачи
  document.querySelectorAll('.task-item').forEach((taskItem) => {
    const description = taskItem.querySelector('.task-desc');
    if (!description) {
      return;
    }

    // Небольшая задержка для корректного расчета размеров
    setTimeout(() => {
      const isClamped = description.scrollHeight > description.clientHeight;

      if (isClamped) {
        const actions = taskItem.querySelector('.task-actions');
        if (actions) {
          const button = document.createElement('button');
          button.type = 'button';
          button.className = 'btn btn-toggle';
          button.textContent = 'Подробнее';

          button.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            
            // Собираем данные задачи для модального окна
            const title = taskItem.querySelector('.task-title').textContent;
            const icon = taskItem.querySelector('.task-icon').textContent;
            const description = taskItem.querySelector('.task-desc').textContent;
            const created = taskItem.querySelector('.task-meta small').textContent;
            const reminderElement = taskItem.querySelector('.reminder-time');
            const reminderTime = reminderElement ? reminderElement.textContent : null;

            const taskData = {
              title: title,
              icon: icon,
              description: description,
              created: created.replace('Создано: ', ''),
              reminderTime: reminderTime ? reminderTime.replace('Напоминание: ', '') : null
            };

            openModal(taskData);
          });

          actions.prepend(button);
        }
      }
    }, 100);
  });
}); 