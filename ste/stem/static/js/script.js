// я использую "this" он делает класс TaskManager полноценным объектом, где все методы могут работать с общими данными (this.modal, this.search, etc.).
// "this" - способ объекта ссылаться на самого себя. 

class TaskManager {  // TaskManager - класс для управления интерфейсом задач
  constructor() {  // constructor - метод инициализации класса
    // Инициализация основных элементов интерфейса
    this.initializeElements();  // this - ссылка на текущий объект класса
    
    // Запуск всех компонентов
    this.setupModalWindows();
    this.setupSearchFunctionality();
    this.setupSortAndFilterFunctionality();
    this.setupDetailButtons();
  }

  // Инициализация элементов DOM
  initializeElements() {  // метод инициализации элементов интерфейса
    // Модальное окно и его компоненты
    this.modal = {  // объект с элементами модального окна
      overlay: document.getElementById('taskModal'),  // getElementById() - метод получения элемента по ID
      closeBtn: document.getElementById('modalCloseBtn'),
      content: document.getElementById('modalContent'),
      title: document.querySelector('.modal-task-title'),  // querySelector() - метод поиска элемента по CSS селектору
      icon: document.querySelector('.modal-task-icon'),
      created: document.getElementById('modalCreated'),
      reminder: document.getElementById('modalReminder'),
      reminderTime: document.getElementById('modalReminderTime')
    };

    // Поисковые элементы
    this.search = {  // объект с элементами поиска
      activeInput: document.getElementById('searchActiveTask'),  // поле поиска активных задач
      completedInput: document.getElementById('searchCompletedTask'),  // поле поиска завершенных задач
      activeCount: document.getElementById('activeResultsCount'),  // activeCount - переменная счетчика результатов поиска
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
    if (this.modal.overlay == null) return;

  // Закрытие модального окна по кнопке
  if (this.modal.closeBtn) {
    const self = this;
    this.modal.closeBtn.addEventListener('click', function() { 
      self.closeModal(); 
    });
  }
  }

  // Открытие модального окна с данными задачи
  openModal(taskItem) {
    // Извлекаем данные напрямую из карточки
    const titleElement = taskItem.querySelector('.task-title');
    let title;
    if (titleElement) {
      title = titleElement.textContent;
    } else {
      title = 'Без названия';
    }
    
    const iconElement = taskItem.querySelector('.task-icon');
    let icon;
    if (iconElement) {
      icon = iconElement.textContent;
    } else {
      icon = '📝';
    }
    
    const descElement = taskItem.querySelector('.task-desc');
    let description;
    if (descElement) {
      description = descElement.textContent;
    } else {
      description = '';
    }
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
  
  // forEach находит все элементы с классом task-item перебирает каждый найденный элемент
  // Для каждого элемента создает кнопку "Подробнее"
  setupDetailButtons() {
    const self = this;
    document.querySelectorAll('.task-item').forEach(function(taskItem) { 
        const actions = taskItem.querySelector('.task-actions');
      if (actions == null) return;

      // Создаем кнопку "Подробнее"
          const button = document.createElement('button');
          button.type = 'button';
          button.className = 'btn btn-toggle';
          button.textContent = 'Подробнее';

      button.addEventListener('click', function() {
        self.openModal(taskItem);
          });

          actions.prepend(button);
          // Кнопка добавляется в НАЧАЛО контейнера actions с помощью prepend()
    });
  }


  // === ФУНКЦИОНАЛ ПОИСКА ===
  // Настройка поиска по названиям задач в реальном времени
  setupSearchFunctionality() {
    const self = this;
    // Поиск для активных задач
    if (this.search.activeInput) {
      this.search.activeInput.addEventListener('input', function() {
        self.performSearch('active', self.search.activeInput.value, self.search.activeCount);
      });
    }
    
    // Поиск для завершенных задач
    if (this.search.completedInput) {
      this.search.completedInput.addEventListener('input', function() {
        self.performSearch('completed', self.search.completedInput.value, self.search.completedCount);
      });
    }
  }

  // Выполнение поиска в указанной секции
  // section - секция для поиска ('active' или 'completed')
  // query - поисковый запрос
  // countElement - элемент счетчика результатов
//   performSearch - функция поиска, которая:
  performSearch(section, query, countElement) {
    const container = this.containers[section];
    if (container == null) return;

    const searchQuery = query.toLowerCase().trim();
    const taskItems = container.querySelectorAll('.task-item:not(.empty-state):not(.hidden-by-filter)');
    
    let visibleCount = 0;
    const totalCount = taskItems.length;

    // Фильтрация задач по поисковому запросу
    taskItems.forEach(function(taskItem) {
      const title = taskItem.querySelector('.task-title');
      let titleText;
      if (title) {
        titleText = title.textContent.toLowerCase();
      } else {
        titleText = '';
      }
      
      let isMatch;
      if (searchQuery == '' || titleText.includes(searchQuery)) {
        isMatch = true;
      } else {
        isMatch = false;
      }
      
      if (isMatch == false) {
        taskItem.classList.add('hidden-by-search');
      } else {
        taskItem.classList.remove('hidden-by-search');
      }
      
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
    if (countElement == null) return;

    if (query == '') {
      countElement.textContent = '';
      return;
    }

    // Правильное склонение для русского языка
    function getResultWord(num) {
      if (num == 1) return 'результат';
      if (num >= 2 && num <= 4) return 'результата';
      return 'результатов';
    }

    countElement.textContent = count + ' ' + getResultWord(count);
  }

  // === ФУНКЦИОНАЛ СОРТИРОВКИ И ФИЛЬТРАЦИИ ===
  // Настройка сортировки и фильтрации задач
  setupSortAndFilterFunctionality() {
    const self = this;
    // Настройка для активных задач
    if (this.sort.activeSelect) {
      this.sort.activeSelect.addEventListener('change', function(event) {
        self.sortTasks('active', event.target.value);
      });
    }
    if (this.filter.activeSelect) {
      this.filter.activeSelect.addEventListener('change', function(event) {
        self.filterTasks('active', event.target.value);
      });
    }
    
    // Настройка для завершенных задач
    if (this.sort.completedSelect) {
      this.sort.completedSelect.addEventListener('change', function(event) {
        self.sortTasks('completed', event.target.value);
      });
    }
    if (this.filter.completedSelect) {
      this.filter.completedSelect.addEventListener('change', function(event) {
        self.filterTasks('completed', event.target.value);
      });
    }
  }

  // Сортировка задач в указанной секции
  // section - секция для сортировки ('active' или 'completed')
  // sortOrder - порядок сортировки ('default', 'date-asc', 'date-desc')
  sortTasks(section, sortOrder) {
    const container = this.containers[section];
    if (container == null || sortOrder == 'default') return;

    // Получаем все задачи (кроме служебных элементов)
    const taskNodeList = container.querySelectorAll('.task-item:not(.empty-state)');
    const taskItems = [];
    for (let i = 0; i < taskNodeList.length; i++) {
      taskItems.push(taskNodeList[i]);
    }
    
    // Сортируем по дате (используем строковое сравнение для простоты)
    const self = this;
    taskItems.sort(function(taskA, taskB) {
      const dateA = self.getTaskDateString(taskA);
      const dateB = self.getTaskDateString(taskB);
      
      if (sortOrder == 'date-asc') {
        if (dateA < dateB) return -1;
        if (dateA > dateB) return 1;
        return 0;
      } else {
        if (dateB < dateA) return -1;
        if (dateB > dateA) return 1;
        return 0;
      }
    });

    // Сохраняем служебный элемент если есть
    const emptyState = container.querySelector('.empty-state');
    
    // Перестраиваем контейнер
    container.innerHTML = '';
    taskItems.forEach(function(item) {
      container.appendChild(item);
    });
    
    // Возвращаем служебный элемент если нужно
    if (emptyState != null) {
      if (taskItems.length == 0) {
        container.appendChild(emptyState);
      }
    }

    // Повторяем поиск если активен
    let searchInput;
    let countElement;
    if (section == 'active') {
      searchInput = this.search.activeInput;
      countElement = this.search.activeCount;
    } else {
      searchInput = this.search.completedInput;
      countElement = this.search.completedCount;
    }
    
    if (searchInput != null) {
      if (searchInput.value.trim() != '') {
        // Повторяем поиск напрямую
        this.performSearch(section, searchInput.value, countElement);
      }
    }
  }

  // Получение строки даты из карточки для сравнения
  // taskItem - карточка задачи
  // Возвращает дату в формате "YYYY-MM-DD HH:MM" для сортировки
  getTaskDateString(taskItem) {
    const metaElement = taskItem.querySelector('.task-meta small');
    if (metaElement == null) return '0000-00-00 00:00';
    
    const dateText = metaElement.textContent;
    // Извлекаем дату в формате дд.мм.гггг чч:мм и конвертируем в гггг-мм-дд чч:мм для сравнения
    const match = dateText.match(/(\d{2})\.(\d{2})\.(\d{4})\s*(\d{2}):(\d{2})/);
    
    if (match) {
      const day = match[1];
      const month = match[2];
      const year = match[3];
      const hours = match[4];
      const minutes = match[5];
      return year + '-' + month + '-' + day + ' ' + hours + ':' + minutes;
    }
    
    return '0000-00-00 00:00'; // Дата по умолчанию
  }


  // Фильтрация задач по типу
  // section - секция ('active' или 'completed')  
  // filterType - тип фильтра ('all', 'notes', 'reminders')
  filterTasks(section, filterType) {
    const container = this.containers[section];
    if (container == null) return;

    container.querySelectorAll('.task-item:not(.empty-state)').forEach(function(task) {
      if (filterType == 'all') {
        task.classList.remove('hidden-by-filter');
      } else {
        let shouldHide = false;
        
        if (filterType == 'notes') {
          if (task.classList.contains('note') == false) {
            shouldHide = true;
          }
        } else if (filterType == 'reminders') {
          if (task.classList.contains('reminder') == false) {
            shouldHide = true;
          }
        }
        
        if (shouldHide) {
          task.classList.add('hidden-by-filter');
        } else {
          task.classList.remove('hidden-by-filter');
        }
      }
    });

    // Обновляем поиск если активен
    let searchInput;
    let countElement;
    if (section == 'active') {
      searchInput = this.search.activeInput;
      countElement = this.search.activeCount;
    } else {
      searchInput = this.search.completedInput;
      countElement = this.search.completedCount;
    }
    
    if (searchInput != null) {
      if (searchInput.value.trim() != '') {
        // Повторяем поиск напрямую
        this.performSearch(section, searchInput.value, countElement);
      }
    }
  }
}

// === ИНИЦИАЛИЗАЦИЯ ===
// Запуск системы управления задачами после загрузки DOM
document.addEventListener('DOMContentLoaded', function() {
  try {
    // Создаем объект менеджера задач (запускаем всю систему)
    window.taskManager = new TaskManager();
  } catch (error) {
    console.error('❌ Ошибка инициализации TaskManager:', error);
  }
}); 