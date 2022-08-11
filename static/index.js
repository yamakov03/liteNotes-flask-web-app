function deleteNote(noteId) {
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({noteId: noteId})
    }).then((_res) => {
        window.location.href = "/";
    });
}

function editNote(noteId) {
    window.location.href = "/edit-note/" + noteId;
}

function duplicateNote(noteId) {
    fetch('/duplicate-note', {
        method: 'POST',
        body: JSON.stringify({noteId: noteId})
    }).then((_res) => {
        window.location.href = "/";
    });
}

function sortNotes(sortBy) {
    window.location.href = "/?sortBy=" + sortBy;
}

function returnHome() {
    window.location.href = "/";
}

