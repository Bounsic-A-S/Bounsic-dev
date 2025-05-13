import {
  ChangeDetectionStrategy,
  Component,
  EventEmitter,
  Input,
  Output,
  inject
} from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  FormBuilder,
  FormGroup,
  ReactiveFormsModule,
  Validators
} from '@angular/forms';
import { ClickOutsideDirective } from '@app/directive/clickoutside.directive';
import { TranslateModule } from '@ngx-translate/core';

@Component({
  selector: 'playlist-modal-create',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, ClickOutsideDirective, TranslateModule],
  templateUrl: './modal_create_playlist.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ModalCreatePlaylistComponent {
  @Input() isOpen = true;
  @Output() closeModal = new EventEmitter<void>();

  isRegisterForm = true;
  isSubmitting = false;
  registerForm: FormGroup;

  private fb = inject(FormBuilder);

  constructor() {
    this.registerForm = this.fb.group({
      username: ['', [Validators.required]],
      email: ['', [Validators.required, Validators.email]],
    });
  }

  close(): void {
    this.closeModal.emit();
  }

}
