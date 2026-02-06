/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstadd_front.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/12 18:59:09 by mel-shdo          #+#    #+#             */
/*   Updated: 2025/12/13 01:48:20 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"
//#include <stdio.h>

void	ft_lstadd_front(t_list **lst, t_list *new)
{
	if (!lst || !new)
		return ;
	new->next = *lst;
	*lst = new;
}

/*int	main(void)
{
	t_list	*head = NULL;
	t_list	*node1;
	t_list	*node2;
	t_list	*node3;

	int		v1 = 1, v2 = 2, v3 = 3;
	node1 = ft_lstnew(&v1);
	node2 = ft_lstnew(&v2);
	node3 = ft_lstnew(&v3);
	ft_lstadd_front(&head, node1);
	ft_lstadd_front(&head, node2);
	ft_lstadd_front(&head, node3);
	t_list *temp = head;
	while (temp)
	{
		printf("%d -> ", *(int *)(temp->content));
		temp = temp->next;
	}
	printf("NULL\n");

	return (0);
}*/