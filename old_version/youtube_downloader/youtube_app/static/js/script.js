const pageNumbers = (total, max, current) => {
    const half = Math.round(max / 2);
    let to = max;

    if(current + half >= total){
        to = total;
    } else if(current > half){
        to - current + half;
    }

    let from = to - max;

    return Array.from({length: max}, (_, i) => (i + 1) + from);
}

function PaginationButtons(totalPages, maxPageVisible = 10, currentPage = 1){
    let pages = pageNumbers(totalPages, maxPageVisible, currentPage);
    let currentPageBtn = null;
    const buttons = new Map();
    const fragment = document.createDocumentFragment();
    const paginationButtonsContainer = document.createElement('div');
    paginationButtonsContainer.className = "pagination-buttons";

    const disabled = {
        start: () => pages[0] === 1,
        prev: () => currentPage === 1,
        end: () => pages.slice(-1)[0] === totalPages,
        next: () => currentPage === totalPages,
    }

    const createAndSetupButton = (label = '', cls = '', disabled = false, handleClick = () => {}) => {
        const button = document.createElement('button');
        button.textContent = label;
        button.className = `page-btn {$cls}`;
        button.disabled = disabled;
        button.addEventListener('click', event => {
            handleClick(event);
            this.update();
            paginationButtonsContainer.value = currentPage;
            paginationButtonsContainer.dispatchEvent(new Event('change'))
        })

        return button;
    }

    const onPageButtonClick = e => currentPage = Number(e.currentTarget.textContent);
    const onPageButtonUpdate = index => btn => {
        btn.textContent = pages[index];

        if(pages[index] === currentPage){
            currentPageBtn.classList.remove('active');
            btn.classList.add('active');
            currentPageBtn = btn;
            currentPageBtn.focus();
        }
    }

    buttons.set(
        createAndSetupButton('start', 'start-page', disabled.start(), () => currentPage = 1),
        (btn) => btn.disabled = disabled.start()
    )

    buttons.set(
        createAndSetupButton('prev', 'prev-page', disabled.prev(), () => currentPage -= 1),
        (btn) => btn.disabled = disabled.prev()
    )

    pages.forEach((pageNumber, index) => {
        const isCurrentPage = pageNumber === currentPage
        const button =
            createAndSetupButton(pageNumber, isCurrentPage ? 'active' : '', false, onPageButtonClick);

        if(isCurrentPage){
            currentPageBtn = button;
        }

        buttons.set(button,onPageButtonUpdate(index))
        })

    buttons.set(
        createAndSetupButton('next', 'next-page', disabled.next(), () => currentPage += 1),
        (btn) => btn.disabled = disabled.next()
    )

    buttons.set(
        createAndSetupButton('end', 'end-page', disabled.end(), () => currentPage = totalPages),
        (btn) => btn.disabled = disabled.end()
    )

    buttons.forEach((_, btn) => fragment.appendChild(btn))

    this.render = (container = document.body) => {
    paginationButtonsContainer.appendChild(fragment)
        container.appendChild(paginationButtonsContainer);
    }

    this.update = (newPageNumber = currentPage) => {
    currentPage = newPageNumber;
    pages = pageNumbers(totalPages, maxPageVisible, currentPage);
    buttons.forEach((updateButton, button) => updateButton(button))
    }

    this.onChange = (handler) => {
        paginationButtonsContainer.addEventListener('change', handler);
    }

};

const paginationButtons = new PaginationButtons(20, 5);

paginationButtons.render();

paginationButtons.onChange(e => {
    console.log(e.target.value)
})
