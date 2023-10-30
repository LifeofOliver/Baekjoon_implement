class RedBlackTree():
    class _Node:
        RED = object()
        BLACK = object()
        __slots__ = '_element', '_parent', '_left', '_right', '_color' 

        def __init__(self, element, parent=None, left=None, right=None, color=RED):
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right
            self._color = color

    def __init__(self):
        self._root = None
        self._size = 0

    def __len__(self):
        return self._size

    def search(self, element):
        current_node=self._root #root부터 검색을 시작한다.
        while current_node != None: #NIL까지 내려가면 검색을 멈춤
            if element == current_node._element: #찾는 값이 현재 노드의 원소의 값과 같으면
                return current_node._element #현재 노드의 값을 반환
            elif element < current_node._element: #찾는 값이 현재 노드의 원소보다 작으면
                current_node = current_node._left  #왼쪽 subtree로 이동
            else: #찾는 값이 현재 노드의 원소보다 크면
                current_node = current_node._right  #오른쪽 subtree로 이동
        return None #NIL에 도달했는데도 찾는 원소가 없으면 None을 반환

    def insert(self, element):
        insert_node = self._Node(element) #삽입하려는 노드객체를 새로 만듦
        if self._root is None: #비어있는 트리면 삽입하는 노드를 root로 만들고, 검은색으로 바꿔줌
            self._root = insert_node
            self._root._color = self._Node.BLACK
        else: #비어있지 않은 tree면
            current_node = self._root #root부터 찾는 search 함수랑 비슷한데
            parent_node = None #삽입노드와 연결해줄 부모노드를 저장할 변수를 만듦
            while current_node is not None: #NIL까지 내려가면 검색을 멈춤
                parent_node = current_node #삽입한 노드와 연결해줄 노드임 (parent node)
                if element < current_node._element:
                    current_node = current_node._left
                elif element > current_node._element:
                    current_node = current_node._right
                else:
                    return
            insert_node._parent = parent_node #삽입한 노드의 부모 노드를 Parent node로 연결
            if element < parent_node._element: #삽입한 노드가 parent노드의 원소보다 작으면 왼쪽자식에
                parent_node._left = insert_node
            else: #크면 오른쪽자식에 연결해줌
                parent_node._right = insert_node
            self._handle_double_red(insert_node) #그리고 삽입한 노드에 대해 double red를 다루는 함수를 적용함
        self._size += 1

    def _handle_double_red(self, node): #double red를 다루는 함수임
        while node._parent != None and node._parent._color == self._Node.RED: #삽입노드의 부모가 RED이고, 노드의 부모가 None이 아니면 계속 진행
            if node._parent == node._parent._parent._left: #삽입노드의 부모가 조부모 노드의 왼쪽 자손일 때
                uncle_node = node._parent._parent._right #삼촌노드는 조부모노드의 오른쪽자식임
                if uncle_node != None and uncle_node._color == self._Node.RED: #(case 1) 삼촌노드가 RED면, recoloring 하는 작업
                    node._parent._color = self._Node.BLACK
                    uncle_node._color = self._Node.BLACK
                    node._parent._parent._color = self._Node.RED
                    if node._parent._parent is None: #조부모노드가 None이면 while roop 종료
                        break
                    else: #조부모노드가 존재시 조부모노드에 대해 handle double black함수 재귀적으로 다시 적용
                        node = node._parent._parent
                else: #삼촌노드가 black이거나 None이면 reconstruction 해주어야 함
                    if node == node._parent._right: #삽입노드가 부모노드의 오른쪽 자식이면 (LR case)
                        node = node._parent #node의 부모를 node변수에 저장 -> 이러면 회전 후 맨 밑에 있는 객체가 node에 저장되어서 이후 LL케이스에서 노드의 지정이 쉽다
                        self._rotate_left(node) #node에 대해 rotate_left 수행(node를 왼쪽 밑으로 내려주는 연산). 이 과정 수행후 LL 케이스로 바뀐다.
                        node._parent._color = self._Node.BLACK #여기서부터는 밑의 LL케이스와 같은 연산임
                        node._parent._parent._color = self._Node.RED
                        self._rotate_right(node._parent._parent)
                        break #reconstruction은 전파가 일어나지 않기 때문에, 한번 하고나면 실행을 멈춘다.
                    else: #LL케이스. 색을 바꿔 준 뒤 조부모를 내려주는 회전을 실시함
                        node._parent._color = self._Node.BLACK 
                        node._parent._parent._color = self._Node.RED
                        self._rotate_right(node._parent._parent)
                        break
                   
            else:  #삽입노드의 부모가 조부모 노드의 오른쪽 자식일 때. 위의 경우와 방향만 반대임
                uncle_node = node._parent._parent._left
                if uncle_node != None and uncle_node._color == self._Node.RED: #삼촌노드가 RED면 recoloring 수행
                    node._parent._color = self._Node.BLACK
                    uncle_node._color = self._Node.BLACK
                    node._parent._parent._color = self._Node.RED
                    if node._parent._parent is None:
                        break
                    else:
                        node = node._parent._parent
                else: #삼촌노드가 None이거나 Black이면 reconstruction 해주어야 함
                    if node == node._parent._left: #삽입노드가 부모노드의 왼쪽 자식이면 (RL case)
                        node = node._parent
                        self._rotate_right(node) #node에 대해 rotate_right 수행(node를 오른쪽 밑으로 내려주는 연산). 이 과정 수행후 RR 케이스로 바뀐다.
                        node._parent._color = self._Node.BLACK 
                        node._parent._parent._color = self._Node.RED
                        self._rotate_left(node._parent._parent)
                        break
                    else:#(RR case)
                        node._parent._color = self._Node.BLACK
                        node._parent._parent._color = self._Node.RED
                        self._rotate_left(node._parent._parent)
                        break
                    
        self._root._color = self._Node.BLACK #마지막으로 root를 BLACK으로 바꾸어준다
    
    def _rotate_left(self, node): #우회전함수. 입력값으로 넣은 노드를 내려줌(왼쪽 방향으로)
        right_child = node._right 
        node._right = right_child._left
        if right_child._left is not None:
            right_child._left._parent = node
        right_child._parent = node._parent
        if node._parent is None:
            self._root = right_child
        elif node._parent._left == node:
            node._parent._left = right_child
        else:
            node._parent._right = right_child
        right_child._left = node
        node._parent = right_child

    def _rotate_right(self, node): #좌회전함수. 입력값으로 넣은 노드를 내려줌(오른쪽 방향으로)
        left_child = node._left 
        node._left = left_child._right
        if left_child._right is not None:
            left_child._right._parent = node
        left_child._parent = node._parent
        if node._parent is None:
            self._root = left_child
        elif node._parent._right == node:
            node._parent._right = left_child
        else:
            node._parent._left = left_child
        left_child._right = node
        node._parent = left_child 

    def delete(self, element): #삭제 함수
        target = self._search_for_delete(element) #삭제할 노드를 찾는다.
        if target == None: #삭제할 노드가 없으면
            return None #None 반환
        target_element = target._element #삭제할 노드의 원소를 저장
        self._delete(target) #실제 삭제 작업
        self._size -= 1
        return target_element

    def _search_for_delete(self, element): #위의 search 함수에서는 원소를 반환해서, 노드를 반환하는 함수를 따로 만들어 줌
        current_node = self._root     
        while current_node != None: 
            if element == current_node._element:    
                return current_node #노드를 반환하게 만들었다.
            elif element < current_node._element:  
                current_node = current_node._left  
            else:   
                current_node = current_node._right  
        return None 
    
    def _delete(self, node): #실제 삭제함수
        if node == self._root: #삭제하려는 노드가 root인 경우를 따로 생각해줌
            if self._root._left is None and self._root._right is None: #tree에 노드 혼자만 있을 때
                self._root = None #tree를 비워버린다
            elif self._root._left is not None and self._root._right is None: #노드의 왼쪽 subtree만 존재할 때에는
                self._root = self._root._left #노드의 왼쪽 자식을 root로 만들고
                self._root._parent = None #원래 root와의 연결을 끊는다
            elif self._root._left is None and self._root._right is not None: #노드의 오른쪽 subtree만 존재할 경우
                self._root = self._root._right #노드의 오른쪽 자식을 root로 만들고
                self._root._parent = None #원래 root와의 연결을 끊는다
            else: #양쪽 subtree가 다 존재할 경우
                successor = self._successor(node) #inorder successor을 찾는다
                self._root._element = successor._element #root의 원소를 successor로 만들어주고
                self._delete(successor) #successor을 삭제하는 과정을 재귀적으로 반복해줌
            if self._root != None: #위의 과정을 거친 후 root가 있으면
                self._root._color = self._Node.BLACK #Black으로 칠해주고
            else: #없으면
                return #함수를 종료한다
        else: #노드가 root가 아닌 경우
            if node._left is not None and node._right is not None: #삭제할 노드가 2개의 subtree를 가질 경우
                    successor = self._successor(node) #대체할 노드를 찾는다.
                    node._element = successor._element #삭제할 노드에 대체할 노드의 원소를 넣는다.
                    node = successor #대체 노드를 삭제하기 위해 node 변수에 대체노드를 저장. 이때 대체노드는 자식을 1개 가지거나, 가지지 않는다.
            child = node._left if node._left is not None else node._right
            parent = node._parent
            if node._color == self._Node.BLACK: #삭제할 노드의 색이 검정색이고
                if child is not None and child._color == self._Node.RED: #자손이 존재하며 그 자손의 색이 빨간색이면
                    child._color = self._Node.BLACK #자식을 BLACK로 칠하고 밑의 if문을 돌림
                else: #만일 자손이 NIL노드거나 검은색이면 (NIL노드도 BLACK으로 취급함)
                    self._handle_double_black(node) #node에 대해 double black을 처리해줌 (node의 child에 대해 처리하기엔 None을 다루기가 너무 까다로움)
            if node == parent._left: #노드가 부모의 왼쪽자식이었다면 (NIL인 경우도 포함임)
                    parent._left = child #노드를 지우고 노드의 자식과 노드의 부모를 연결해줌
            else: #오른쪽 자식인 경우에도 같음 (NIL인 경우도 포함임)
                parent._right = child
            if child is not None: #NIL인 경우엔 이 작업이 필요하지 않지만, 실제 노드인 경우에는 부모로 연결하는 작업이 필요함
                child._parent = parent #부모로 향하는 링크를 연결해줌
        
    
    def _handle_double_black(self, node): #더블블랙을 처리하는 함수
        while node != self._root and node._color == self._Node.BLACK: #노드가 root인 경우에는 위에서 처리를 해줬기 때문에 제외, 그리고 노드가 RED인 경우에도 이 작업이 필요하지 않음
            if node == node._parent._left: #노드가 부모의 왼쪽자식인 경우를 먼저 생각
                sibling = node._parent._right #sibling은 부모의 오른쪽자식임
                if sibling._color == self._Node.RED: # case 1: sibling이 red인 경우
                    sibling._color = self._Node.BLACK #형제를 BLACK으로 칠하고
                    node._parent._color = self._Node.RED #부모를 RED로 칠하고
                    self._rotate_left(node._parent) #부모를 기준으로 좌회전해서 부모를 밑으로 내려준다.
                    sibling = node._parent._right #좌회전 하고 나면 case 2번이나 case 3번이 되기 때문에, 상황 처리를 위해 sibiling을 다시 지정

                if (sibling._left is None or sibling._left._color == self._Node.BLACK) and (sibling._right is None or sibling._right._color == self._Node.BLACK): 
                    #case 2: 형제가 black이거나 None이고, 형제의 자식이 모두 black이거나 NIL일 경우
                    sibling._color = self._Node.RED #형제를 RED로 칠하고
                    node = node._parent #parent에 대해 while 문 안에서 다시 double black 상황을 판단하고 처리해줌 (rocoloring -> propagate)
                else: #형제가 black이긴 한데, 자식 중 하나라도 red가 섞여 있는 경우. rotation의 방향 때문에 케이스가 2가지로 갈린다.
                    if sibling._right is None or sibling._right._color == self._Node.BLACK:
                        # case 3: 형제가 black이고, 형제의 왼쪽 자식이 red이고 오른쪽자식이 black이거나 NIL일 경우 (zig-zag 케이스와 비슷)
                        sibling._left._color = self._Node.BLACK #형제의 왼쪽 자식을 BLACK으로 칠해준다
                        sibling._color = self._Node.RED #형제의 색은 RED로 칠해줌 
                        self._rotate_right(sibling) #형제를 우회전하여 밑으로 내려준다
                        sibling = node._parent._right #형제를 다시 참조하도록 바꿔줌. 이 경우 case 4가 되었다고 볼 수 있음
                    # Case 4: sibling이 black이고, 오른쪽자식이 red고 왼쪽자식이 black이거나 NIL인 경우
                    sibling._color = node._parent._color #형제가 부모의 자리로 올라갈꺼니까 색깔을 맞춰줌
                    node._parent._color = self._Node.BLACK #부모의 색을 검은색으로 칠해줌
                    sibling._right._color = self._Node.BLACK #오른쪽 자식을 검은색으로 칠해줌
                    self._rotate_left(node._parent) #부모를 밑으로 내려주는 좌회전을 실시한다.
                    break #이 경우에는 double black이 위로 전파되지는 않으므로 루프를 끝낸다.
            else: #노드가 부모의 오른쪽 자식인 경우. 위의 부분과 방향만 바뀐다.
                sibling = node._parent._left
                if sibling._color == self._Node.RED:
                    sibling._color = self._Node.BLACK
                    node._parent._color = self._Node.RED
                    self._rotate_right(node._parent)
                    sibling = node._parent._left

                if (sibling._left is None or sibling._left._color == self._Node.BLACK) and \
                        (sibling._right is None or sibling._right._color == self._Node.BLACK):
                    sibling._color = self._Node.RED
                    node = node._parent
                else:
                    if sibling._left is None or sibling._left._color == self._Node.BLACK:
                        if sibling._right:
                            sibling._right._color = self._Node.BLACK
                        sibling._color = self._Node.RED
                        self._rotate_left(sibling)
                        sibling = node._parent._left

                    sibling._color = node._parent._color
                    node._parent._color = self._Node.BLACK
                    sibling._left._color = self._Node.BLACK
                    self._rotate_right(node._parent)
                    break
        node._color = self._Node.BLACK #마지막으로 node의 색을 검은색으로 칠해준다

    # BONUS FUNCTIONS -- use them freely if you want
    def _is_black(self, node):
        return node == None or node._color == self._Node.BLACK

    def _successor(self, node):
        successor = node._right
        while successor._left != None:
            successor = successor._left
        return successor

    def _sibiling(self, node):
        parent = node._parent

        if parent._left == node:
            return parent._right
        else:
            return parent._left

    # Supporting functions -- DO NOT MODIFY BELOW
    def display(self):
        print('--------------')
        self._display(self._root, 0)
        print('--------------')

    def _display(self, node, depth):
        if node == None:
            return

        if node._right != None:
            if node._right._parent != node:
                print("parent-child error - ", node._element, node._right._element)
            self._display(node._right, depth+1)

        if node == self._root:
            symbol = '>'
        else:
            symbol = '*'

        if node._color == self._Node.RED:
            colorstr = 'R'
        else:
            colorstr = 'B'
        print(f'{"    "*depth}{symbol} {node._element}({colorstr})')
        if node._left != None:
            if node._left._parent != node:
                print("parent error - ", node._element, node._left._element)
            self._display(node._left, depth+1)

    def inorder_traverse(self):
        return self._inorder_traverse(self._root)

    def _inorder_traverse(self, node):
        if node == None:
            return []
        else:
            return self._inorder_traverse(node._left) + [node._element] + self._inorder_traverse(node._right)

    def check_tree_property_silent(self):
        if self._root == None:
            return True

        if not self._check_parent_child_link(self._root):
            print('Parent-child link is violated')
            return False
        if not self._check_binary_search_tree_property(self._root):
            print('Binary search tree property is violated')
            return False
        if not self._root._color == self._Node.BLACK:
            print('Root black property is violated')
            return False
        if not self._check_double_red_property(self._root):
            print('Internal property is violated')
            return False
        if self._check_black_height_property(self._root) == 0:
            print('Black height property is violated')
            return False
        return True

    def check_tree_property(self):
        if self._root == None:
            print('Empty tree')
            return

        print('Checking binary search tree property...')
        self._check_parent_child_link(self._root)
        self._check_binary_search_tree_property(self._root)
        print('Done')

        print('Checking root black property...')
        print(self._root._color == self._Node.BLACK)
        print('Done')

        print('Checking internal property (=no double red)...')
        self._check_double_red_property(self._root)
        print('Done')

        print('Checking black height property...')
        self._check_black_height_property(self._root)
        print('Done')

    def _check_parent_child_link(self, node):
        if node == None:
            return True

        test_pass = True

        if node._right != None:
            if node._right._parent != node:
                print("parent-child error - ", node._element, node._right._element)
            test_pass = test_pass and self._check_parent_child_link(node._right)
        if node._left != None:
            if node._left._parent != node:
                print("parent error - ", node._element, node._left._element)
            test_pass = test_pass and self._check_parent_child_link(node._left)

        return test_pass

    def _check_binary_search_tree_property(self, node):
        if node == None:
            return True

        test_pass = True

        if node._left != None:
            if node._left._element > node._element:
                print("Binary search tree property error - ", node._element, node._left._element)
                return False
            test_pass = test_pass and self._check_binary_search_tree_property(node._left)

        if node._right != None:
            if node._right._element < node._element:
                print("Binary search tree property error - ", node._element, node._right._element)
                return False
            test_pass = test_pass and self._check_binary_search_tree_property(node._right)

        return test_pass

    def _check_double_red_property(self, node):
        if node == None:
            return True

        test_pass = True

        if node._color == self._Node.RED:
            if node._left != None:
                if node._left._color == self._Node.RED:
                    print("Double red property error - ", node._element, node._left._element)
                    return False
            if node._right != None:
                if node._right._color == self._Node.RED:
                    print("Double red property error - ", node._element, node._right._element)
                    return False

        if node._left != None:
            test_pass = test_pass and self._check_double_red_property(node._left)
        if node._right != None:
            test_pass = test_pass and self._check_double_red_property(node._right)

        return test_pass


    def _check_black_height_property(self, node):
        if node == None:
            return 1

        left_height = self._check_black_height_property(node._left)
        right_height = self._check_black_height_property(node._right)

        if left_height != right_height:
            print("Black height property error - ", node._element, left_height, right_height)
            return 0

        if node._color == self._Node.BLACK:
            return left_height + 1
        else:
            return left_height