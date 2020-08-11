<template>
  <div id="todo">
    <h1>Todo App</h1>
    <div>
      <label for="title">Todo：</label>
      <input type="text" v-model="title" placeholder="Title" />
    </div>
    <div>
      <input type="submit" value="Create" @click="createTodo" />
    </div>
    <ul v-for="todo in todoList" v-bind:key="todo.id">
      <li>
        {{ todo.title }}
        <button @click="deleteTodo(todo.id)">Delete</button>
      </li>
    </ul>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import axios from 'axios';
import { v4 as uuidv4 } from 'uuid';

interface TodoItem {
  id: string;
  title: string;
}

interface DataType {
  title: string;
  todoList: TodoItem[];
}

export default Vue.extend({
  name: 'Todo',
  data(): DataType {
    return {
      title: '',
      todoList: new Array<TodoItem>()
    };
  },
  mounted() {
    this.loadTodo();
  },
  methods: {
    loadTodo: async function() {
      const getAllTodo = async () => {
        try {
          return await axios({
            method: 'GET',
            url: '/api/get_all_todo'
          });
        } catch {
          return;
        }
      };
      const response = await getAllTodo();
      if (!response || response.status !== 200) {
        alert('Todo getting error\nReflesh the page');
        return;
      }
      this.todoList = response.data;
    },
    createTodo: async function() {
      if (this.title === '') {
        alert('Enter todo');
        return;
      }
      const todo = { id: uuidv4(), title: this.title };
      const createTodoOnDB = async () => {
        try {
          return await axios({
            method: 'POST',
            headers: { 'content-Type': 'application/json' },
            data: JSON.stringify(todo),
            url: '/api/create_todo'
          });
        } catch {
          return;
        }
      };
      const response = await createTodoOnDB();
      if (!response || response.status !== 200) {
        alert('Todo creation error');
        return;
      }
      this.todoList.push(todo);
      this.title = '';
    },
    deleteTodo: async function(id: string) {
      const deleteTodoOnDB = async () => {
        try {
          return await axios({
            method: 'DELETE',
            headers: { 'content-Type': 'application/json' },
            data: JSON.stringify({ id }),
            url: '/api/delete_todo'
          });
        } catch {
          return;
        }
      };
      const response = await deleteTodoOnDB();
      if (!response || response.status !== 200) {
        alert('Todo deletion error');
        return;
      }
      this.todoList = this.todoList.filter(todo =>
        todo.id === id ? null : todo
      );
    }
  }
});
</script>
