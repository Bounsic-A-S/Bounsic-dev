// search-filter.component.ts
import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ClickOutsideDirective } from '@app/directive/clickoutside.directive';
import { TranslateModule } from '@ngx-translate/core';
@Component({
  selector: 'dashboard-searchBar',
  templateUrl: 'search-bar.component.html',
  imports: [CommonModule, TranslateModule, FormsModule, ClickOutsideDirective],
})
export class SearchBarComponent {
  searchQuery: string = '';
  filterTags: string[] = ['Género', 'Ritmo', 'Letra'];
  selectedTags: string[] = [];

  songToSearch: string = ''

  public searchResults: string[] = []
  public isSearchBarOnFocus = true

  search() {
    this.searchResults.push("Song1")

  }
  setResultsUi(value:boolean) {
    this.isSearchBarOnFocus = value
  }

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