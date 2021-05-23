window.addEventListener(`load`, function(){
  let req = new XMLHttpRequest();
  req.open("GET", "/api/tasks/", true);
  req.onload = function(){
      if (this.status >= 200 && this.status < 400){
          let data = JSON.parse(this.response)
          renderRes(data.todos);
      }
  }
  req.send();
  const tasksListElement = document.querySelector(`.tasks__list`);
  const doneTasksListElement = document.querySelector(`.tasks__list__done`);

  function renderRes(data){
    for (item in data){
      if (data[item].state == "todo" ){
        var insert_in = tasksListElement
        var elementClass = 'tasks__item'
      } else{
        var insert_in = doneTasksListElement
        var elementClass = 'tasks__done__item'
      }
        let element = insert_in.insertAdjacentHTML("beforeend",
        `<li class='${elementClass}' id="${data[item].id}" draggable="true">
        <a href='#' data-toggle="modal"  data-target="#updateModal" class="task__item_header">
          <h5>${data[item].subject}</h5>
        </a>
        <p>${data[item].text}</p>
        </li>`
        );
      }

    const taskElements = tasksListElement.querySelectorAll(`.tasks__item`);
    const doneTasksListElements = doneTasksListElement.querySelectorAll(`.tasks__done__item`);

    for (const task of taskElements){
        task.draggable = true;
    }
    for (const task of doneTasksListElements){
        task.draggable = true;
    }

    tasksListElement.addEventListener(`dragstart`, (evt) => {
        evt.target.classList.add(`selected`);
    });
    doneTasksListElement.addEventListener(`dragstart`, (evt) => {
        evt.target.classList.add(`selected`);
    });

    tasksListElement.addEventListener(`dragend`, (evt) => {
        evt.target.classList.remove(`selected`);
    });
    doneTasksListElement.addEventListener(`dragend`, (evt) => {
        evt.target.classList.remove(`selected`);
    });

    var  updateTaskEvent = document.querySelectorAll('.task__item_header')

    for (const update of updateTaskEvent){
      update.addEventListener('click', (evt) =>{
        getTaskById(evt.target.parentElement.parentElement.id)
      })
    }
}

function getTaskById(id){
  fetch(`/api/task/${id}/`, {
    method: "GET",
  })
  .then( (response) => {
          if (response.status !== 200) {
        return Promise.reject();
          }
  return response.json()
  })
  .then(i => insertTaskDataToUpdateForm(i))
  .catch(error => console.error(error))
}

function insertTaskDataToUpdateForm(data){
  let formSubject = document.querySelector('#task_subject');
  let formText = document.querySelector('#task_text');
  let updateFormTaskId = document.querySelector('.update_form_task_id')
  let updateFormTaskCurrentState = document.querySelector('.update_form_task_current_state')
  updateFormTaskId.value = data.data.id
  updateFormTaskCurrentState.value = data.data.state
  formSubject.value = data.data.subject
  formText.value = data.data.text
}
//
let updateTaskBtn = document.querySelector('.update_task_btn')
updateTaskBtn.addEventListener('click', updateTask)

function updateTask() {
  let formSubject = document.querySelector('#task_subject').value;
  let formText = document.querySelector('#task_text').value;
  let updateFormTaskId = document.querySelector('.update_form_task_id').value;
  let updateFormTaskCurrentState= document.querySelector('.update_form_task_current_state').value;
  let data = new FormData();
  data.append('subject', formSubject);
  data.append('text', formText);
  data.append('todo_id', updateFormTaskId);
  data.append('state', updateFormTaskCurrentState);
  fetch(`/api/task/${updateFormTaskId}/`, {
    method: "PUT",
    body: data,
  })
  .then((response) => {
    if (response.status !== 201) {
      return Promise.reject();
    }
    return response.json()
  })
  .then(i => updateTaskView(i))
  .catch(error => console.error(error))
}
//
function updateTaskView(data){
  let element = document.getElementById(`${data.id}`)
  element.children[0].children[0].innerText = data.subject
  element.children[1].innerText = data.text
  $('#updateModal').modal('toggle')

}
//
function renderNew(data){
    let element = tasksListElement.insertAdjacentHTML("beforeend",
    `<li class='tasks__item' id="${data.id}" draggable="true" class="task__item_header">
    <a href='#' data-toggle="modal"  data-target="#updateModal" class="task__item_header">
    <h5>${data.subject}</h5>
    </a>
    <p>${data.text}</p>
    </li>`);
    const lastAddedTask = document.getElementById(data.id)
    lastAddedTask.addEventListener('click',  getTaskById(data.id))
};

let delete_task_btn = document.querySelector('.delete_task_btn')
delete_task_btn.addEventListener('click', deleteTask)

function deleteTask(){
  if (confirm("Подтвердите удаление задачи")) {
    let updateFormTaskId = document.querySelector('.update_form_task_id').value;
    let data = new FormData();
    data.append('todo_id', updateFormTaskId);
    fetch(`/api/task/${updateFormTaskId}/`, {
      method: "DELETE",
      body: data,
    })
    .then( (response) => {
      if (response.status !== 200) {
        return Promise.reject();
      }
      return response.json()
    })
    .then((i) => console.log(i))
    .catch((error) => console.error(error))
    document.getElementById(`${updateFormTaskId}`).remove();
    $('#updateModal').modal('toggle')
  } else {
      txt = "You pressed Cancel!";
  }
}
//
const getNextElement = (cursorPosition, currentElement) => {
  const currentElementCoord = currentElement.getBoundingClientRect();
  const currentElementCenter = currentElementCoord.y + currentElementCoord.height / 2;

  const nextElement = (cursorPosition < currentElementCenter) ?
    currentElement :
    currentElement.nextElementSibling;

  return nextElement;
};
//
tasksListElement.addEventListener(`dragover`, (evt) => {
  evt.preventDefault();
  const activeElement = tasksListElement.querySelector(`.selected`);
  let activeElementTaskDone = doneTasksListElement.querySelector(`.selected`);
  const currentElement = evt.target;
  const isMoveable = activeElement !== currentElement &&
  currentElement.classList.contains(`tasks__item`) | currentElement.classList.contains(`tasks__done__item`) ;

  if (!isMoveable) {
    return;
  }

  if (activeElementTaskDone) {
    activeElementTaskDone.classList.remove('tasks__done__item')
    activeElementTaskDone.classList.add('tasks__item')
  	tasksListElement.appendChild(activeElementTaskDone);
    changeTaskStatus('todo', activeElementTaskDone.id)

  } else {
    var nextElement = getNextElement(evt.clientY, currentElement);

    doneTasksListElement.addEventListener(`dragover`, (evt) =>{
      if (!nextElement){
          doneTasksListElement.appendChild(activeElement);
        }
    })

    if (
      nextElement &&
      activeElement === nextElement.previousElementSibling ||
      activeElement === nextElement
    ) {
      return;
    }

    tasksListElement.insertBefore(activeElement, nextElement);
  }
});
//
doneTasksListElement.addEventListener(`dragover`, (evt) => {
  evt.preventDefault();

  const activeElement = doneTasksListElement.querySelector(`.selected`);
  var activeElementTodoTask = tasksListElement.querySelector(`.selected`);
  let currentElement = evt.target;
  const isMoveable = activeElement | activeElementTodoTask !== currentElement &&
    currentElement.classList.contains(`tasks__done__item`) | currentElement.classList.contains(`tasks__item`);

  if (!isMoveable) {
    return;
  }
//
  if (activeElementTodoTask) {
  activeElementTodoTask.classList.remove('tasks__item')
  activeElementTodoTask.classList.add('tasks__done__item')
  doneTasksListElement.appendChild(activeElementTodoTask);
  changeTaskStatus('done', activeElementTodoTask.id)
  } else {
    var nextElement = getNextElement(evt.clientY, currentElement);
//
  if (
    nextElement &&
    activeElement === nextElement.previousElementSibling ||
    activeElement === nextElement
  ) {
    return;
  }
  doneTasksListElement.insertBefore(activeElement, nextElement);

  }
});
//
function changeTaskStatus(new_state, task_id){
  let data = new FormData();
  data.append('state', new_state);
  data.append('todo_id', task_id);
  fetch(`/api/task/${task_id}/`, {
    method: "PUT",
      body: data,
  })
  .then( (response) => {
    if (response.status !== 201) {
      return Promise.reject();
    }
  return response.json()
  })
  .then(i => console.log(i))
  .catch(error => console.error(error))
}
//
const sendNewTaskBtn = document.querySelector('.send_new_task')
sendNewTaskBtn.addEventListener('click', function(evt){
    evt.preventDefault();
    let newTaskSubject = document.querySelector('#new_task_subject').value
    let newTaskText = document.querySelector('#new_task_text').value
    addNewTask(newTaskSubject, newTaskText)
    $('#exampleModal').modal('toggle')
});
//
function addNewTask(newTaskSubject, newTaskText){
  let new_task_form = document.querySelector('#new_task_form')
  let data = new FormData();
  data.append('new_task_subject', newTaskSubject);
  data.append('new_task_text', newTaskText);
  fetch("/api/task/add/", {
    method: "POST",
      body: data,
  })
  .then( (response) => {
          if (response.status !== 201) {
        return Promise.reject();
          }
  return response.json()
  })
  .then(i => renderNew(i))
  .catch(error => console.error(error))
}
});
