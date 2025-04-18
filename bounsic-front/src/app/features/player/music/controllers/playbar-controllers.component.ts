import { CommonModule } from '@angular/common';
import {
  ChangeDetectionStrategy,
  Component,
  CUSTOM_ELEMENTS_SCHEMA,
  EventEmitter,
  Input,
  Output,
} from '@angular/core';
import { HoverExitDirective } from '@app/directive/onhoverexit.directive';
import { LucideAngularModule, Volume2, VolumeX, List } from 'lucide-angular';
@Component({
  selector: 'player-music-playbar-controllers',
  standalone: true,
  imports: [LucideAngularModule, CommonModule,HoverExitDirective],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  templateUrl: './playbar-controllers.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class PlayerBarControllersComponent {
  //icons
  readonly Volume2 = Volume2;
  readonly VolumeX = VolumeX;
  readonly List = List;
  //inputs
  @Input() isMuted!: boolean;
  @Input() volume!: number;
  @Output() toggleMute = new EventEmitter<void>();
  @Output() onVolumeChange = new EventEmitter<number>();
  //vars
  public isVolumeOpen = false;

  openVolume() {
    console.log('hi');
    this.isVolumeOpen = true;
  }
  closeVolume() {
    console.log('bye');
    this.isVolumeOpen = false;
  }
  onVolumeChange_(event: Event) {
    const value = (event.target as HTMLInputElement).value;
    this.onVolumeChange.emit(parseFloat(value));
  }
}
