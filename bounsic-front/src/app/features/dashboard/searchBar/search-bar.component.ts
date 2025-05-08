// search-filter.component.ts
import { CommonModule } from '@angular/common';
import { ChangeDetectorRef, Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { ClickOutsideDirective } from '@app/directive/clickoutside.directive';
import { SongService } from '@app/services/song.service';
import { TranslateModule } from '@ngx-translate/core';
import DashboardSong from 'src/types/dashboard/DashboardSong';
import { LoaderComponent } from "../../../shared/ui/loaders/loader.component";
@Component({
  selector: 'dashboard-searchBar',
  templateUrl: 'search-bar.component.html',
  imports: [CommonModule, TranslateModule, FormsModule, ClickOutsideDirective, RouterModule, LoaderComponent],
})
export class SearchBarComponent {
  private searchService = inject(SongService)
  private cdRef = inject(ChangeDetectorRef);  
  searchQuery: string = '';
  filterTags: string[] = ['Género', 'Ritmo', 'Letra'];
  selectedTags: string[] = [];

  songToSearch: string = ''

  public searchResults: DashboardSong[] = []
  public isSearchBarOnFocus = true

  //loading
  public loading: boolean = false;

  search(): void {
    this.searchResults = [];  
    this.loading = true;

    this.searchService.searchSongByTitle(this.songToSearch).subscribe({
      next: (songs: DashboardSong[]) => {
        this.searchResults = songs;  
        this.loading = false;
        this.setResultsUi(true)
        this.cdRef.detectChanges();  
      },
      error: err => {
        console.error('Error en la búsqueda:', err);
        this.loading = false;  
        this.cdRef.detectChanges();  
      }
    });
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