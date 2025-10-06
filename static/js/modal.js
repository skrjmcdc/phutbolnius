"use strict";

const modal = document.getElementById('this-is-a-modal');

function showModal() {
    modal.classList.remove('hidden');
}

function hideModal() {
    modal.classList.add('hidden');
}
