// search-filter.component.ts
import { CommonModule } from '@angular/common';
import { ChangeDetectorRef, Component, EventEmitter, inject, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { ClickOutsideDirective } from '@app/directive/clickoutside.directive';
import { SongService } from '@app/services/song.service';
import { TranslateModule, TranslateService } from '@ngx-translate/core';
import DashboardSong from 'src/types/dashboard/DashboardSong';
import { LoaderComponent } from "../../../shared/ui/loaders/loader.component";
import { LucideAngularModule, Trash } from 'lucide-angular';
@Component({
  selector: 'dashboard-searchBar',
  templateUrl: 'search-bar.component.html',
  imports: [CommonModule, TranslateModule, FormsModule, ClickOutsideDirective, RouterModule, LoaderComponent, LucideAngularModule],
})
export class SearchBarComponent {
  TrashIcon = Trash
  private searchService = inject(SongService)
  private cdRef = inject(ChangeDetectorRef);

  private translateService = inject(TranslateService)

  searchQuery: string = '';
  filterTags: string[] = [this.translateService.instant('BOUNSIC.DASHBOARD.FILTERS.GENRE'),
  this.translateService.instant('BOUNSIC.DASHBOARD.FILTERS.RHYTHM'), this.translateService.instant('BOUNSIC.DASHBOARD.FILTERS.LYRIC')];

  selectedTags: string[] = [];

  songToSearch: string = ''

  public searchResults: DashboardSong[] = []
  public isSearchBarOnFocus = true

  //loading
  public loading: boolean = false;

  @Output() searchTriggered = new EventEmitter<DashboardSong[]>(); // resultados de búsqueda

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
  handleSongClick(song_id: string): void {

    this.searchService.searchSongsAlikeByLyrics(song_id).subscribe({
      next: (songs: DashboardSong[]) => {
        this.searchResults = songs;
        this.loading = false;
        this.setResultsUi(false)
        this.cdRef.detectChanges();
        this.searchTriggered.emit(songs);
        this.searchResults = []
      },
      error: err => {
        console.error('Error en la búsqueda:', err);
        this.loading = false;
        this.cdRef.detectChanges();
      }
    });
  }

  clearFilters(): void {
    this.searchTriggered.emit([]);
    this.selectedTags = [];
  }

  setResultsUi(value: boolean) {
    this.isSearchBarOnFocus = value
  }

  toggleTag(tag: string): void {
    if (tag === this.translateService.instant('BOUNSIC.DASHBOARD.FILTERS.GENRE') || tag === this.translateService.instant('BOUNSIC.DASHBOARD.FILTERS.RHYTHM')) return

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