const deleteBtns = document.querySelectorAll('.deleteBtn')

deleteBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const xhr = new XMLHttpRequest();
        const filename = btn.parentElement.parentElement.id;
        xhr.onreadystatechange = function () {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    var rowToDelete = document.getElementById(filename);
                    rowToDelete.parentNode.removeChild(rowToDelete);
                } else if (xhr.readyState === XMLHttpRequest.DONE && xhr.status !== 200) {
                    alert(xhr.response.message);
                } else {
                    alert('エラーが発生しました。');
                }
            }
        };
        xhr.open('DELETE', '/video/' + filename + '/delete', true);
        xhr.send();
    });
})
