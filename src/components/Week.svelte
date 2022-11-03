<script>
    import { get_day, get_date, to_ymd, is_today } from "src/date.js";
    export let params = {};

    let path = `/move/${params.edu}/${params.school}`;

    /** @type {Date[]} */
    let date_list = [];

    /** @type {Date} */
    let center = params.date;

    for (let i = -3; i <= 3; i++) {
        let date = new Date(center.valueOf() + 24 * 3600 * 1000 * i);
        date_list.push(date);
    }
</script>

<div class="menu weeks-btn">
    {#if is_today(params.date) == false}
        <a class="btn" href="#{path}">오늘 메뉴로 이동하기</a>
        <br style="margin-bottom:15px" />
    {/if}
    {#each date_list as date}
        <a
            class="btn {is_today(date) ? 'today' : ''}"
            href="#{path}/{to_ymd(date)}"
            on:click="{(event) => {
                if (to_ymd(date) == to_ymd(params.date)) {
                    event.preventDefault();
                }
            }}">
            {get_day(date)}
            <br />
            <sub>{get_date(date)}일</sub>
        </a>
    {/each}
</div>

<style>
    a:not(:last-child) {
        margin-right: 3px;
    }

    .btn.today {
        background-color: #5a5a5a;
        color: #dbdbdb;
    }
</style>
