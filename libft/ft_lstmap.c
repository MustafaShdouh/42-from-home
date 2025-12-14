/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstmap.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/13 01:40:43 by mel-shdo          #+#    #+#             */
/*   Updated: 2025/12/13 01:48:20 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"
//#include <stdio.h>

t_list	*ft_lstmap(t_list *lst, void *(*f)(void *), void (*del)(void *))
{
	t_list	*newlist;
	t_list	*newnode;
	void	*content;

	if (!lst || !f || !del)
		return (NULL);
	newlist = NULL;
	while (lst)
	{
		content = f(lst->content);
		newnode = ft_lstnew(content);
		if (!newnode)
		{
			del(content);
			ft_lstclear(&newlist, del);
			return (NULL);
		}
		ft_lstadd_back(&newlist, newnode);
		lst = lst->next;
	}
	return (newlist);
}

/*void	*add_ten(void *content)
{
	int	*res;
	
	res = malloc(sizeof(int));
	if (!res)
		return (NULL);
	*res = *(int *)content + 10;
	return (res);
}

void	del(void *content)
{
	free(content);
}

int	main(void)
{
	t_list	*list = NULL;
	t_list	*map_list = NULL;
	t_list	*temp;
	int		v1 = 1, v2 = 2, v3 = 3;

	ft_lstadd_back(&list, ft_lstnew(&v1));
	ft_lstadd_back(&list, ft_lstnew(&v2));
	ft_lstadd_back(&list, ft_lstnew(&v3));
	map_list = ft_lstmap(list, add_ten, del);
	printf("Original: ");
	temp = list;
	while (temp) { printf("%d -> ", *(int *)temp->content); temp = temp->next; }
	printf("NULL\n");
	printf("Mapped  : ");
	temp = map_list;
	while (temp) { printf("%d -> ", *(int *)temp->content); temp = temp->next; }
	printf("NULL\n");
	ft_lstclear(&map_list, del);
	t_list *curr = list;
	t_list *next;
	while (curr) { next = curr->next; free(curr); curr = next; }
}*/