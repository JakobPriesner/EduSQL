import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ErmDialogComponent } from './erm-dialog.component';

describe('ErmDialogComponent', () => {
  let component: ErmDialogComponent;
  let fixture: ComponentFixture<ErmDialogComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ErmDialogComponent]
    });
    fixture = TestBed.createComponent(ErmDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
