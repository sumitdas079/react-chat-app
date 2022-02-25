import firebase from 'firebase/compat/app';
import 'firebase/compat/auth';
import 'firebase/compat/firestore';

const firebaseApp = firebase.initializeApp({
    apiKey: "AIzaSyCluOEvokpBCHmkbQLetUminHAoS5w40pM",
    authDomain: "react-firebase-chat-dd3d9.firebaseapp.com",
    projectId: "react-firebase-chat-dd3d9",
    storageBucket: "react-firebase-chat-dd3d9.appspot.com",
    messagingSenderId: "298381211345",
    appId: "1:298381211345:web:c67d599560ca6d12b8b7f0"
})

const db = firebaseApp.firestore()
const auth = firebase.auth()

export { db, auth }