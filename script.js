const BASE_URL = "http://localhost:5500";  // ✅ This is correct!
 // Flask usually runs here

const taskForm = document.getElementById('TaskForm');
const taskInput = document.getElementById('TaskInput');
const taskList = document.getElementById('Tasklist');

async function fetchTasks() {
  const res = await fetch(`${BASE_URL}/tasks`);
  const tasks = await res.json();
  renderTasks(tasks);
}

async function addTask(taskText) {
  await fetch(`${BASE_URL}/tasks`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title: taskText, completed: false })
  });
  fetchTasks();
}

async function deleteTask(id) {
  await fetch(`${BASE_URL}/tasks/${id}`, { method: 'DELETE' });
  fetchTasks();
}

async function toggleTask(id, completed) {
  await fetch(`${BASE_URL}/tasks/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ completed: !completed })
  });
  fetchTasks();
}

function renderTasks(tasks) {
  taskList.innerHTML = '';
  tasks.forEach(task => {
    const li = document.createElement('li');
    li.textContent = task.title;
    if (task.completed) li.classList.add('completed');

    li.addEventListener('click', () => toggleTask(task.id, task.completed));

    const delBtn = document.createElement('button');
    delBtn.textContent = 'Delete';
    delBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      deleteTask(task.id);
    });

    li.appendChild(delBtn);
    taskList.appendChild(li);
  });
}

taskForm.addEventListener('submit', (e) => {
  e.preventDefault();
  const text = taskInput.value.trim();
  if (text) {
    addTask(text);
    taskInput.value = '';
  }
});

fetchTasks();
