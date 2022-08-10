function deleteNote(noteId) {
    fetch('https://litenotes.herokuapp.com/delete-note', {
        method: 'POST',
        body: JSON.stringify({noteId: noteId}),
        headers: {
            'Content-Type': 'application/json',
        }
    }).then((_res) => {
        window.location.href = "/";
    });
}

function editNote(noteId) {
    window.location.href = "/edit-note/" + noteId;
}

function duplicateNote(noteId) {
    fetch('https://litenotes.herokuapp.com/duplicate-note', {
        method: 'POST',
        body: JSON.stringify({noteId: noteId}),
        headers: {
            'Content-Type': 'application/json',
        }
    }).then((_res) => {
        window.location.href = "/";
    });
}

function returnHome() {
    window.location.href = "/";
}

