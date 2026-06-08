// ---------- DASHBOARD MODALS ----------
console.log("SCRIPT LOADED");
window.onload = function () {

    const incomeBtn = document.querySelector('.income-btn');
    const expenseBtn = document.querySelector('.expense-btn');

    const modal = document.getElementById('incomeModal');
    const expenseModal = document.getElementById('expenseModal');

    const incomeClose = document.getElementById('incomeClose');
    const expenseClose = document.getElementById('expenseClose');

    // Open modals
    if (incomeBtn && modal) {
        incomeBtn.onclick = function () {
            modal.style.display = "block";
        };
    }

    if (expenseBtn && expenseModal) {
        expenseBtn.onclick = function () {
            expenseModal.style.display = "block";
        };
    }

    // Close modals
    if (incomeClose && modal) {
        incomeClose.onclick = function () {
            modal.style.display = "none";
        };
    }

    if (expenseClose && expenseModal) {
        expenseClose.onclick = function () {
            expenseModal.style.display = "none";
        };
    }
};



// ---------- EDIT MODAL ----------

document.addEventListener("DOMContentLoaded", function () {

    const modal = document.getElementById("editModal");
    const closeBtn = document.getElementById("edit-close");
    const dropdown = document.getElementById("edit-category");
    
    if (!modal) return;

    const incomeCategories = [
        "Salary", "Business", "Freelance", "Investment", "Gift", "Other"
    ];

    const expenseCategories = [
        "Food", "Rent", "Transport", "Shopping",
        "Bills", "Entertainment", "Medical", "Other"
    ];

    document.querySelectorAll(".edit-btn").forEach(function(button){

        button.addEventListener("click", function(){

            console.log("Clicked");

            const id = this.dataset.id;
            const category = this.dataset.category;
            const amount = this.dataset.amount;
            const date = this.dataset.date;
            const type = this.dataset.type;

            document.getElementById("edit-id").value = id;
            document.getElementById("edit-amount").value = amount;
            document.getElementById("edit-date").value = date;

            dropdown.innerHTML = "";

            let list = (type === "income") ? incomeCategories : expenseCategories;

            list.forEach(function(cat){
                let option = document.createElement("option");
                option.value = cat;
                option.textContent = cat;

                if(cat === category){
                    option.selected = true;
                }

                dropdown.appendChild(option);
            });

            modal.style.display = "flex";
        });

    });

    if(closeBtn){
        closeBtn.addEventListener("click", function(){
            modal.style.display = "none";
        });
    }

});