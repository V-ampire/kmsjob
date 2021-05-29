"use strict";


class MessageCtrl {
    constructor(container) {
        this.container = container;
    }

    renderMessages(messages) {
        const msgList = document.createElement('ul');
        msgList.className = 'list-group text-center';
        console.log(messages);
        for (let message of messages) {
            console.log(message);
            const li = document.createElement('li');
            li.className = `list-group-item message ${message.tags}`;
            li.textContent = message.msg;
            msgList.appendChild(li);
        }
        this.container.appendChild(msgList);
    }
}