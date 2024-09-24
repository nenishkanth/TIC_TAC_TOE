const cells = document.querySelectorAll('.cell');
const status = document.getElementById('status');
const resetButton = document.getElementById('reset');

// Handle cell clicks
cells.forEach(cell => {
    cell.addEventListener('click', () => {
        const index = cell.getAttribute('data-index');
        if (!cell.textContent) { // Prevent overwriting moves
            makeMove(index);
        }
    });
});

// Make a player move
function makeMove(index) {
    fetch('/move', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ position: index }),
    })
    .then(response => response.json())
    .then(data => {
        updateBoard(index, 'X');
        if (data.winner) {
            displayWinner(data.winner);
        } else if (data.ai_position !== undefined) {
            updateBoard(data.ai_position, 'O');
            if (data.winner) {
                displayWinner(data.winner);
            }
        }
    })
    .catch(error => console.error('Error making move:', error));
}

// Update the board UI
function updateBoard(index, player) {
    cells[index].textContent = player;
    if (player === 'X') {
        cells[index].classList.add('clicked-by-user1');
    } else if (player === 'O') {
        cells[index].classList.add('clicked-by-user2');
    }
}

// Display winner or tie
function displayWinner(winner) {
    if (winner === 'tie') {
        status.textContent = 'It\'s a tie!';
    } else {
        status.textContent = `${winner} wins!`;
    }
    // Disable further moves
    cells.forEach(cell => cell.style.pointerEvents = 'none');
}

// Reset the game
resetButton.addEventListener('click', () => {
    fetch('/reset', { method: 'POST' })
        .then(() => {
            cells.forEach(cell => {
                cell.textContent = '';
                cell.style.pointerEvents = 'auto'; // Re-enable clicking
                cell.className = 'cell'; // Reset the cell class
            });
            status.textContent = '';
        })
        .catch(error => console.error('Error resetting game:', error));
});
