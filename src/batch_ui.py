"""
배치 선택 UI 모듈

PRD v1.3.0 섹션 3.3 "배치 선택 창"에 정의된 UI를 구현합니다.
"""

import customtkinter as ctk
from typing import List, Dict, Callable, Optional


class BatchSelectionDialog(ctk.CTkToplevel):
    """배치 선택 다이얼로그"""

    def __init__(self, parent, batch_info: Dict, on_confirm: Callable, on_cancel: Callable):
        """
        Args:
            parent: 부모 윈도우
            batch_info: scan_batch_folders() 결과
            on_confirm: 확인 버튼 콜백 (selected_batches: List[str])
            on_cancel: 취소 버튼 콜백
        """
        super().__init__(parent)

        self.batch_info = batch_info
        self.on_confirm_callback = on_confirm
        self.on_cancel_callback = on_cancel

        # 배치 정렬 (REGULAR 첫 번째, EXTRA 번호순)
        from .batch_merger import sort_batches
        self.batch_names = sort_batches(list(batch_info.keys()))

        # 체크박스 변수
        self.checkboxes: Dict[str, 'BatchCheckbox'] = {}

        # UI 설정
        self.title("배치 선택")
        self.resizable(False, True)

        # 창 크기 계산 (배치 개수에 따라 동적 조절)
        base_height = 250
        checkbox_height = 35 * len(self.batch_names)
        total_height = min(base_height + checkbox_height, 700)  # 최대 700

        self.geometry(f"500x{total_height}")

        # 모달 설정
        self.transient(parent)
        self.grab_set()

        # UI 생성
        self._create_widgets()

        # 창 중앙 배치
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")

    def _create_widgets(self):
        """UI 위젯 생성"""
        # 헤더
        header = ctk.CTkLabel(
            self,
            text="병합할 배치를 선택해주세요",
            font=("맑은 고딕", 16, "bold"),
            text_color="#1e293b"
        )
        header.pack(pady=(20, 15))

        # 스크롤 가능한 프레임
        scroll_frame = ctk.CTkScrollableFrame(
            self,
            width=450,
            height=min(300, 35 * len(self.batch_names))
        )
        scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # 체크박스 생성
        for batch_name in self.batch_names:
            is_required = (batch_name == 'REGULAR')
            checkbox = BatchCheckbox(scroll_frame, batch_name, is_required, self.batch_info[batch_name])
            self.checkboxes[batch_name] = checkbox

        # 버튼 프레임
        button_frame1 = ctk.CTkFrame(self, fg_color="transparent")
        button_frame1.pack(pady=5)

        # 전체 선택/해제 버튼
        btn_select_all = ctk.CTkButton(
            button_frame1,
            text="전체 선택",
            width=120,
            height=32,
            command=self._select_all
        )
        btn_select_all.pack(side="left", padx=5)

        btn_deselect_all = ctk.CTkButton(
            button_frame1,
            text="전체 해제",
            width=120,
            height=32,
            command=self._deselect_all
        )
        btn_deselect_all.pack(side="left", padx=5)

        # 확인/취소 버튼 프레임
        button_frame2 = ctk.CTkFrame(self, fg_color="transparent")
        button_frame2.pack(pady=(5, 20))

        btn_confirm = ctk.CTkButton(
            button_frame2,
            text="확인",
            width=120,
            height=36,
            fg_color="#1e293b",
            hover_color="#334155",
            command=self._on_confirm
        )
        btn_confirm.pack(side="left", padx=5)

        btn_cancel = ctk.CTkButton(
            button_frame2,
            text="취소",
            width=120,
            height=36,
            fg_color="transparent",
            border_width=2,
            border_color="#1e293b",
            text_color="#1e293b",
            hover_color="#f1f5f9",
            command=self._on_cancel
        )
        btn_cancel.pack(side="left", padx=5)

    def _select_all(self):
        """전체 선택"""
        for batch_name, checkbox in self.checkboxes.items():
            if batch_name != 'REGULAR':  # REGULAR는 이미 체크됨
                checkbox.set_checked(True)

    def _deselect_all(self):
        """전체 해제 (REGULAR 제외)"""
        for batch_name, checkbox in self.checkboxes.items():
            if batch_name != 'REGULAR':  # REGULAR는 해제 불가
                checkbox.set_checked(False)

    def _on_confirm(self):
        """확인 버튼 클릭"""
        # 선택된 배치 수집
        selected = [
            batch_name
            for batch_name, checkbox in self.checkboxes.items()
            if checkbox.is_checked()
        ]

        # 콜백 호출
        if self.on_confirm_callback:
            self.on_confirm_callback(selected)

        self.destroy()

    def _on_cancel(self):
        """취소 버튼 클릭"""
        if self.on_cancel_callback:
            self.on_cancel_callback()

        self.destroy()


class BatchCheckbox:
    """배치 체크박스"""

    def __init__(self, parent, batch_name: str, is_required: bool, batch_data: Dict):
        """
        Args:
            parent: 부모 위젯
            batch_name: 배치명
            is_required: 필수 여부 (REGULAR)
            batch_data: 배치 정보
        """
        self.batch_name = batch_name
        self.is_required = is_required

        # 변수
        self.var = ctk.BooleanVar(value=True)  # 기본 체크

        # 표시 텍스트 (기본 정보만)
        display_text = batch_name
        if is_required:
            display_text += " (필수)"

        # 체크박스
        self.checkbox = ctk.CTkCheckBox(
            parent,
            text=display_text,
            variable=self.var,
            state="disabled" if is_required else "normal",  # REGULAR는 비활성화 (항상 체크)
            font=("맑은 고딕", 12)
        )
        self.checkbox.pack(pady=3, padx=20, anchor="w")

    def is_checked(self) -> bool:
        """체크 상태 반환"""
        return self.var.get()

    def set_checked(self, checked: bool):
        """체크 상태 설정 (REGULAR는 변경 불가)"""
        if not self.is_required:
            self.var.set(checked)
