<script>
  import Icon from "svelte-awesome";
  import { faPlus, faTrash } from "@fortawesome/free-solid-svg-icons";
  export let title = "Title";
  export let items = null;
  export let changed = false;

  function addItem() {
    changed = true;
    items.push({
      trigger: "",
      response: "",
    });
    items = items;
  }

  function removeItem(index) {
    changed = true;
    items.splice(index, 1);
    items = items;
  }
</script>

<span><b>{title}</b></span>

<div>
  {#if items.length}
    <ul>
      {#each items as item, i}
        {#if i == items.length - 1}
          <li>
            <input type="text" bind:value={item.trigger} /><span> :</span>
            <input type="text" bind:value={item.response} />
            <span on:click={() => removeItem(i)} class="icon remove">
              <Icon data={faTrash} />
            </span>
            <span on:click={addItem} class="icon add">
              <Icon data={faPlus} />
            </span>
          </li>
        {:else}
          <li>
            <input type="text" bind:value={item.trigger} /><span> :</span>
            <input type="text" bind:value={item.response} />
            <span on:click={() => removeItem(i)} class="icon remove">
              <Icon data={faTrash} />
            </span>
          </li>
        {/if}
      {/each}
    </ul>
  {:else}
    <span>No items defined</span>
    <span on:click={addItem} class="icon add">
      <Icon data={faPlus} />
    </span>
  {/if}
</div>

<style>
  .icon {
    cursor: pointer;
    margin-left: 3px;
  }
  .add {
    color: green;
  }

  .remove {
    color: crimson;
  }
</style>
