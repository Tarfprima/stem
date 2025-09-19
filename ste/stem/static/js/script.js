class TaskManager {
  constructor() {
    // Инициализация основных элементов интерфейса
    this.initializeElements();
    
    // Запуск всех компонентов
    this.setupModalWindows();
    this.setupSearchFunctionality();
    this.setupSortAndFilterFunctionality();
    this.setupDetailButtons();
  }

  // Инициализация элементов DOM
  initializeElements() {
    // Модальное окно и его компоненты
    this.modal = {
      overlay: document.getElementById('taskModal'),
      closeBtn: document.getElementById('modalCloseBtn'),
      content: document.getElementById('modalContent'),
      title: document.querySelector('.modal-task-title'),
      icon: document.querySelector('.modal-task-icon'),
      created: document.getElementById('modalCreated'),
      reminder: document.getElementById('modalReminder'),
      reminderTime: document.getElementById('modalReminderTime')
    };

    // Поисковые элементы
    this.search = {
      activeInput: document.getElementById('searchActiveTask'),
      completedInput: document.getElementById('searchCompletedTask'),
      activeCount: document.getElementById('activeResultsCount'),
      completedCount: document.getElementById('completedResultsCount')
    };

    // Элементы сортировки
    this.sort = {
      activeSelect: document.getElementById('sortActiveTask'),
      completedSelect: document.getElementById('sortCompletedTask')
    };

    // Элементы фильтрации
    this.filter = {
      activeSelect: document.getElementById('filterActiveTask'),
      completedSelect: document.getElementById('filterCompletedTask')
    };

    // Контейнеры задач
    this.containers = {
      active: document.querySelector('.tasks-grid[data-section="active"]'),
      completed: document.querySelector('.tasks-grid[data-section="completed"]')
    };
  }


  // === МОДАЛЬНЫЕ ОКНА ===
  // Настройка функционала всплывающих окон для просмотра задач
  setupModalWindows() {
    if (!this.modal.overlay) return;

    // Закрытие модального окна по кнопке
    this.modal.closeBtn?.addEventListener('click', () => this.closeModal());
  }

  // Открытие модального окна с данными задачи
  openModal(taskItem) {
    // Извлекаем данные напрямую из карточки
    const title = taskItem.querySelector('.task-title')?.textContent || 'Без названия';
    const icon = taskItem.querySelector('.task-icon')?.textContent || '📝';
    const description = taskItem.querySelector('.task-desc')?.textContent || '';
    const createdElement = taskItem.querySelector('.task-meta small');
    const reminderElement = taskItem.querySelector('.reminder-time');
    
    // Заполнение содержимого модального окна
    if (this.modal.title) this.modal.title.textContent = title;
    if (this.modal.icon) this.modal.icon.textContent = icon;
    if (this.modal.content) this.modal.content.textContent = description;
    if (this.modal.created && createdElement) {
      this.modal.created.textContent = createdElement.textContent.replace('Создано: ', '');
    }
    
    // Обработка времени напоминания
    if (reminderElement && this.modal.reminderTime) {
      this.modal.reminderTime.textContent = reminderElement.textContent.replace('Напоминание: ', '');
      this.modal.reminder.style.display = 'block';
    } else if (this.modal.reminder) {
      this.modal.reminder.style.display = 'none';
    }
    
    // Показ модального окна
    this.modal.overlay.classList.add('show');
  }

  // Закрытие модального окна
  closeModal() {
    this.modal.overlay.classList.remove('show');
  }

  // === КНОПКИ "ПОДРОБНЕЕ" ===
  // Создание кнопок для всех задач
  setupDetailButtons() {
    document.querySelectorAll('.task-item').forEach((taskItem) => {
      const actions = taskItem.querySelector('.task-actions');
      if (!actions) return;

      // Создаем кнопку "Подробнее"
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'btn btn-toggle';
      button.textContent = 'Подробнее';

      button.addEventListener('click', (event) => {
        event.preventDefault();
        event.stopPropagation();
        
        this.openModal(taskItem);
      });

      actions.prepend(button);
    });
  }


  // === ФУНКЦИОНАЛ ПОИСКА ===
  // Настройка поиска по названиям задач в реальном времени
  setupSearchFunctionality() {
    // Поиск для активных задач
    if (this.search.activeInput) {
      this.search.activeInput.addEventListener('input', () => {
        this.performSearch('active', this.search.activeInput.value, this.search.activeCount);
      });
    }
    
    // Поиск для завершенных задач
    if (this.search.completedInput) {
      this.search.completedInput.addEventListener('input', () => {
        this.performSearch('completed', this.search.completedInput.value, this.search.completedCount);
      });
    }
  }

  // Выполнение поиска в указанной секции
  // section - секция для поиска ('active' или 'completed')
  // query - поисковый запрос
  // countElement - элемент счетчика результатов
  performSearch(section, query, countElement) {
    const container = this.containers[section];
    if (!container) return;

    const searchQuery = query.toLowerCase().trim();
    const taskItems = container.querySelectorAll('.task-item:not(.empty-state):not(.hidden-by-filter)');
    
    let visibleCount = 0;
    const totalCount = taskItems.length;

    // Фильтрация задач по поисковому запросу
    taskItems.forEach(taskItem => {
      const title = taskItem.querySelector('.task-title');
      const titleText = title?.textContent.toLowerCase() || '';
      
      const isMatch = !searchQuery || titleText.includes(searchQuery);
      
      taskItem.classList.toggle('hidden-by-search', !isMatch);
      if (isMatch) visibleCount++;
    });

    // Обновляем счетчик результатов
    this.updateResultsCount(countElement, searchQuery, visibleCount);
  }


  // Обновление счетчика результатов поиска
  // countElement - элемент счетчика
  // query - поисковый запрос
  // count - количество найденных результатов
  updateResultsCount(countElement, query, count) {
    if (!countElement) return;

    if (!query) {
      countElement.textContent = '';
      return;
    }

    // Правильное склонение для русского языка
    const getResultWord = (num) => {
      if (num === 1) return 'результат';
      if (num >= 2 && num <= 4) return 'результата';
      return 'результатов';
    };

    countElement.textContent = `${count} ${getResultWord(count)}`;
  }

  // === ФУНКЦИОНАЛ СОРТИРОВКИ И ФИЛЬТРАЦИИ ===
  // Настройка сортировки и фильтрации задач
  setupSortAndFilterFunctionality() {
    // Настройка для активных задач
    if (this.sort.activeSelect) {
      this.sort.activeSelect.addEventListener('change', (event) => {
        this.sortTasks('active', event.target.value);
      });
    }
    if (this.filter.activeSelect) {
      this.filter.activeSelect.addEventListener('change', (event) => {
        this.filterTasks('active', event.target.value);
      });
    }
    
    // Настройка для завершенных задач
    if (this.sort.completedSelect) {
      this.sort.completedSelect.addEventListener('change', (event) => {
        this.sortTasks('completed', event.target.value);
      });
    }
    if (this.filter.completedSelect) {
      this.filter.completedSelect.addEventListener('change', (event) => {
        this.filterTasks('completed', event.target.value);
      });
    }
  }

  // Сортировка задач в указанной секции
  // section - секция для сортировки ('active' или 'completed')
  // sortOrder - порядок сортировки ('default', 'date-asc', 'date-desc')
  sortTasks(section, sortOrder) {
    const container = this.containers[section];
    if (!container || sortOrder === 'default') return;

    // Получаем все задачи (кроме служебных элементов)
    const taskItems = Array.from(container.querySelectorAll('.task-item:not(.empty-state)'));
    
    // Сортируем по дате (используем строковое сравнение для простоты)
    taskItems.sort((taskA, taskB) => {
      const dateA = this.getTaskDateString(taskA);
      const dateB = this.getTaskDateString(taskB);
      
      return sortOrder === 'date-asc' ? dateA.localeCompare(dateB) : dateB.localeCompare(dateA);
    });

    // Сохраняем служебный элемент если есть
    const emptyState = container.querySelector('.empty-state');
    
    // Перестраиваем контейнер
    container.innerHTML = '';
    taskItems.forEach(item => container.appendChild(item));
    
    // Возвращаем служебный элемент если нужно
    if (emptyState && taskItems.length === 0) {
      container.appendChild(emptyState);
    }

    // Повторяем поиск если активен
    const searchInput = section === 'active' ? this.search.activeInput : this.search.completedInput;
    if (searchInput?.value.trim()) {
      searchInput.dispatchEvent(new Event('input'));
    }
  }

  // Получение строки даты из карточки для сравнения
  // taskItem - карточка задачи
  // Возвращает дату в формате "YYYY-MM-DD HH:MM" для сортировки
  getTaskDateString(taskItem) {
    const metaElement = taskItem.querySelector('.task-meta small');
    if (!metaElement) return '0000-00-00 00:00';
    
    const dateText = metaElement.textContent;
    // Извлекаем дату в формате дд.мм.гггг чч:мм и конвертируем в гггг-мм-дд чч:мм для сравнения
    const match = dateText.match(/(\d{2})\.(\d{2})\.(\d{4})\s*(\d{2}):(\d{2})/);
    
    if (match) {
      const [, day, month, year, hours, minutes] = match;
      return `${year}-${month}-${day} ${hours}:${minutes}`;
    }
    
    return '0000-00-00 00:00'; // Дата по умолчанию
  }


  // Фильтрация задач по типу
  // section - секция ('active' или 'completed')  
  // filterType - тип фильтра ('all', 'notes', 'reminders')
  filterTasks(section, filterType) {
    const container = this.containers[section];
    if (!container) return;

    // Простая фильтрация по классам
    container.querySelectorAll('.task-item:not(.empty-state)').forEach(taskItem => {
      const showTask = filterType === 'all' || 
                       (filterType === 'notes' && taskItem.classList.contains('note')) ||
                       (filterType === 'reminders' && taskItem.classList.contains('reminder'));
      
      taskItem.classList.toggle('hidden-by-filter', !showTask);
    });

    // Обновляем поиск если активен
    const searchInput = section === 'active' ? this.search.activeInput : this.search.completedInput;
    if (searchInput?.value.trim()) {
      searchInput.dispatchEvent(new Event('input'));
    }
  }
}

// === ИНИЦИАЛИЗАЦИЯ ===
// Запуск системы управления задачами после загрузки DOM
document.addEventListener('DOMContentLoaded', () => {
  try {
    // Создаем объект менеджера задач (запускаем всю систему)
    window.taskManager = new TaskManager();
  } catch (error) {
    console.error('❌ Ошибка инициализации TaskManager:', error);
  }
});