import {Component, ElementRef, ViewChild} from '@angular/core';
import {MatDialogRef} from "@angular/material/dialog";

class DialogOverviewExampleDialog {
}

@Component({
  selector: 'app-erm-dialog',
  templateUrl: './erm-dialog.component.html',
  styleUrls: ['./erm-dialog.component.css']
})
export class ErmDialogComponent {

  zoomLevel = 1;
  xPos = 0;
  yPos = 0;

  constructor(
    public dialogRef: MatDialogRef<DialogOverviewExampleDialog>
  ) {}

  zoomIn() {
    this.zoomLevel += 0.1;
  }

  zoomOut() {
    if (this.zoomLevel > 0.1) {
      this.zoomLevel -= 0.1;
    }
  }

  toggleFullScreen(element: HTMLElement) {
    if (!document.fullscreenElement) {
      element.requestFullscreen().catch(console.error);
    } else if (document.exitFullscreen) {
      document.exitFullscreen();
    }
  }

  onNoClick(): void {
    this.dialogRef.close();
  }

  onWheel(event: WheelEvent): void {
    event.preventDefault();

    const scaleStep = 0.1;
    const rect = (event.target as HTMLElement).getBoundingClientRect();
    const x = event.clientX - rect.left; // x position within the element.
    const y = event.clientY - rect.top;  // y position within the element.

    if (event.deltaY < 0) {
      // Zoom in
      this.zoomLevel += scaleStep;
    } else {
      // Zoom out
      this.zoomLevel -= scaleStep;
      this.zoomLevel = Math.max(this.zoomLevel, scaleStep); // prevent zooming out beyond original size
    }

    // Calculate new position
    this.xPos = x - (x * this.zoomLevel);
    this.yPos = y - (y * this.zoomLevel);
  }

}
