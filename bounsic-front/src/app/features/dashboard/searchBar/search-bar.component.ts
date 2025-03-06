// search-filter.component.ts
import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';

@Component({
  selector: 'dashboard-searchBar',
  templateUrl: 'search-bar.component.html',
  imports: [CommonModule],
})
export class SearchBarComponent {
  searchQuery: string = '';
  filterTags: string[] = ['Género', 'Ritmo', 'Letra'];
  selectedTags: string[] = [];

  toggleTag(tag: string): void {
    const index = this.selectedTags.indexOf(tag);
    if (index === -1) {
      this.selectedTags.push(tag);
    } else {
      this.selectedTags.splice(index, 1);
    }
  }

  isTagSelected(tag: string): boolean {
    return this.selectedTags.includes(tag);
  }
}