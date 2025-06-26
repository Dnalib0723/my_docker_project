// my_project/web-frontend/html/script.js
document.addEventListener('DOMContentLoaded', () => {
    const fetchDataBtn = document.getElementById('fetchDataBtn');
    const passengerListDiv = document.getElementById('passengerList');
    const tableBody = document.getElementById('tableBody');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const errorMessage = document.getElementById('errorMessage');

    fetchDataBtn.addEventListener('click', fetchPassengers);

    async function fetchPassengers() {
        loadingIndicator.classList.remove('hidden');
        errorMessage.classList.add('hidden');
        tableBody.innerHTML = ''; // 清空之前的資料

        try {
            // 注意：這裡使用 /api/passengers，因為 Nginx 會將 /api/ 代理到後端 API 服務
            const response = await fetch('/api/passengers');
            if (!response.ok) {
                throw new Error(`HTTP 錯誤! 狀態: ${response.status}`);
            }
            const data = await response.json();
            
            if (data.length === 0) {
                tableBody.innerHTML = '<tr><td colspan="7" class="py-3 px-6 text-center">沒有找到乘客資料。</td></tr>';
            } else {
                data.forEach(passenger => {
                    const row = document.createElement('tr');
                    row.classList.add('border-b', 'border-gray-200', 'hover:bg-gray-100');
                    row.innerHTML = `
                        <td class="py-3 px-6 text-left whitespace-nowrap">${passenger.PassengerId}</td>
                        <td class="py-3 px-6 text-left whitespace-nowrap">${passenger.Name}</td>
                        <td class="py-3 px-6 text-left whitespace-nowrap">${passenger.Sex}</td>
                        <td class="py-3 px-6 text-left whitespace-nowrap">${passenger.Age !== null ? passenger.Age : 'N/A'}</td>
                        <td class="py-3 px-6 text-left whitespace-nowrap">${passenger.Survived === 1 ? '是' : '否'}</td>
                        <td class="py-3 px-6 text-left whitespace-nowrap">${passenger.Pclass}</td>
                        <td class="py-3 px-6 text-left whitespace-nowrap">${passenger.Fare !== null ? passenger.Fare.toFixed(2) : 'N/A'}</td>
                    `;
                    tableBody.appendChild(row);
                });
            }
        } catch (error) {
            console.error('獲取乘客資料時發生錯誤:', error);
            errorMessage.classList.remove('hidden');
            tableBody.innerHTML = ''; // 確保表格在錯誤時是空的
        } finally {
            loadingIndicator.classList.add('hidden');
        }
    }
});
