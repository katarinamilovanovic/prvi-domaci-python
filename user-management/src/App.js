import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css';

function App() {
  const [users, setUsers] = useState([]);
  const [newUser, setNewUser] = useState({name: '', age: '', address: '', id: ''});
  const [selectedUser, setSelectedUser] = useState(null);
  const [updateUser, setUpdateUser] = useState({ name: '', age: '', address: '', id: '' });



useEffect(() => {
  fetchUsers();
}, []);

const fetchUsers = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/user/list');
    setUsers(response.data);    
  } catch (error) {
    console.error('Error fetching users:', error);
  }
};

const handleCreateUser = async() => {
  try {
    await axios.post('http://127.0.0.1:5000/user/add', {
      ...newUser, 
      age: parseInt(newUser.age), 
      id: parseInt(newUser.id),
    });
    fetchUsers();
    console.log(newUser)
    setNewUser({ name: '', age: '', address:'', id:''});
    
  } catch (error) {
    console.error('Error creating user:', error)
  }
};

const handleSelectUser = async (id) => {
  try {
    const response = await axios.get(`http://127.0.0.1:5000/user/get/${id}`);
    setSelectedUser(response.data);
    setUpdateUser({
      name: response.data.name,
      age: response.data.age,
      address: response.data.address,
      id: response.data.id
    });
  } catch (error) {
    console.error('Error fetching user:', error);
  }
};

const handleUpdateUser = async (id) => {
  try {
    await axios.put(`http://127.0.0.1:5000/user/update/${id}`, {
      ...updateUser,
      age: parseInt(updateUser.age),
      id: parseInt(updateUser.id)
    });
    fetchUsers();
    setSelectedUser(null);
  } catch (error) {
    console.error('Error updating user:', error);
  }
};

const handleDeleteUser = async (id) => {
  try {
    await axios.delete(`http://127.0.0.1:5000/user/delete/${id}`);
    fetchUsers();
  } catch (error) {
    console.error('Error deleting user:', error);
  }
};

return (
  <div className="App">
    <h1>User Management</h1>

    <div>
      <h2>Create User</h2>
      <input
        type="text"
        placeholder="Name"
        value={newUser.name}
        onChange={(e) => setNewUser({ ...newUser, name: e.target.value })}
      />
      <input
        type="number"
        placeholder="Age"
        value={newUser.age}
        onChange={(e) => setNewUser({ ...newUser, age: e.target.value })}
      />
      <input
        type="text"
        placeholder="Address"
        value={newUser.address}
        onChange={(e) => setNewUser({ ...newUser, address: e.target.value })}
      />
       <input
        type="text"
        placeholder="Id"
        value={newUser.id}
        onChange={(e) => setNewUser({ ...newUser, id: e.target.value })}
      />
      <button onClick={handleCreateUser}>Create</button>
    </div>

    <div>
      <h2>Users List</h2>
      <ul>
        {users.map((user) => (
          <li key={user.id}>
            {user.name}, {user.age}, {user.address}
            <button onClick={() => handleSelectUser(user.id)}>Edit</button>
            <button onClick={() => handleDeleteUser(user.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>

    {selectedUser && (
      <div>
        <h2>Edit User</h2>
        <input
          type="text"
          placeholder="Name"
          value={updateUser.name}
          onChange={(e) => setUpdateUser({ ...updateUser, name: e.target.value })}
        />
        <input
          type="number"
          placeholder="Age"
          value={updateUser.age}
          onChange={(e) => setUpdateUser({ ...updateUser, age: e.target.value })}
        />
        <input
          type="text"
          placeholder="Address"
          value={updateUser.address}
          onChange={(e) => setUpdateUser({ ...updateUser, address: e.target.value })}
        />
        <button onClick={() => handleUpdateUser(selectedUser.id)}>Update</button>
      </div>
    )}
  </div>
);

}

export default App;
