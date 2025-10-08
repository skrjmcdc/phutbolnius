"use strict";

function showToast(title, message, type, duration=5000) {

    const toastBox = document.getElementById('toast-box');
    const toastTitle = document.getElementById('toast-title');
    const toastMessage = document.getElementById('toast-message');

    if (!toastBox) {
        return;
    }

    toastTitle.textContent = title;
    toastMessage.textContent = message;

    toastBox.classList.remove('opacity-0', 'translate-y-64');
    toastBox.classList.add('opacity-100', 'translate-y-0');

    setTimeout(() => {
        toastBox.classList.remove('opacity-100', 'translate-y-0');
        toastBox.classList.add('opacity-0', 'translate-y-64');
    }, duration);

}
