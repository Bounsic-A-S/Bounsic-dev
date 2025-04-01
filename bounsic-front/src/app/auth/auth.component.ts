import { CommonModule } from '@angular/common';
import {
  ChangeDetectionStrategy,
  Component,
  Input,
  Output,
  EventEmitter,
} from '@angular/core';

@Component({
  selector: 'app-auth',
  standalone: true,
  imports: [CommonModule],
  styleUrl:'./auth.css',
  templateUrl: './auth.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class AuthComponent {
  @Input() isOpen: boolean = false; // Para controlar la visibilidad
  @Output() closeModal: EventEmitter<void> = new EventEmitter(); // Emitir evento para cerrar el modal

  close() {
    this.closeModal.emit();
  }
}
